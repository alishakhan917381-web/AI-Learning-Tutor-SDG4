import unittest
from unittest.mock import MagicMock, patch
import json
import os
from app import app, generate_ai_response

class GeminiChatbotProjectTestCase(unittest.TestCase):
    def setUp(self):
        """Set up Flask test client."""
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

    def test_security_and_config_files(self):
        """Verify .gitignore and .env.example exist and .env is never tracked."""
        gitignore_path = os.path.join(self.base_dir, ".gitignore")
        self.assertTrue(os.path.exists(gitignore_path), ".gitignore is missing")
        with open(gitignore_path, "r", encoding="utf-8") as f:
            gitignore_content = f.read()
            self.assertIn(".env", gitignore_content, ".env must be listed in .gitignore")

        example_env_path = os.path.join(self.base_dir, ".env.example")
        self.assertTrue(os.path.exists(example_env_path), ".env.example is missing")
        with open(example_env_path, "r", encoding="utf-8") as f:
            example_env_content = f.read()
            self.assertIn("GEMINI_API_KEY=", example_env_content)

        # Check app.py to guarantee no hard-coded API key exists
        app_path = os.path.join(self.base_dir, "app.py")
        with open(app_path, "r", encoding="utf-8") as f:
            app_content = f.read()
            self.assertNotIn("AIzaSy", app_content, "API key must never be hardcoded in app.py")

    def test_file_structure(self):
        """Verify all essential project files exist and have non-zero size."""
        required_files = [
            "app.py",
            "requirements.txt",
            "run.bat",
            "README.md",
            ".gitignore",
            ".env.example",
            os.path.join("templates", "index.html"),
            os.path.join("static", "css", "style.css"),
            os.path.join("static", "js", "script.js")
        ]
        for rel_path in required_files:
            full_path = os.path.join(self.base_dir, rel_path)
            self.assertTrue(os.path.exists(full_path), f"Missing file: {rel_path}")
            self.assertGreater(os.path.getsize(full_path), 0, f"File is empty: {rel_path}")

    def test_home_route(self):
        """Verify home page loads correctly with status 200 and all required UI elements."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)

        self.assertIn("CampusBot", html)
        self.assertIn('id="chat-box"', html, "Chat box element is required")
        self.assertIn('id="user-input"', html, "Message input is required")
        self.assertIn('id="send-btn"', html, "Send button is required")
        self.assertIn('id="clear-chat-btn"', html, "Clear Chat button is required")
        self.assertIn('id="typing-indicator"', html, "Loading/typing indicator is required")

    def test_static_assets(self):
        """Verify CSS and JS assets are served properly and contain code formatting."""
        css_resp = self.client.get("/static/css/style.css")
        self.assertEqual(css_resp.status_code, 200)
        css_text = css_resp.get_data(as_text=True)
        css_resp.close()
        self.assertIn("chat-container", css_text)
        self.assertIn("code-block-wrapper", css_text)

        js_resp = self.client.get("/static/js/script.js")
        self.assertEqual(js_resp.status_code, 200)
        js_text = js_resp.get_data(as_text=True)
        js_resp.close()
        self.assertIn("formatBotMessage", js_text)
        self.assertIn("___CODE_BLOCK_", js_text)

    def test_chat_api_missing_key_guidance(self):
        """When GEMINI_API_KEY is not configured, reply provides clear setup instructions."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": ""}, clear=False):
            response = self.client.post(
                "/api/chat",
                data=json.dumps({"message": "Hello bot"}),
                content_type="application/json"
            )
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(data.get("status"), "success")
            self.assertIn("Gemini API Key Required", data.get("reply", ""))
            self.assertIn(".env", data.get("reply", ""))

    @patch("app.get_gemini_client")
    def test_chat_api_with_mocked_gemini(self, mock_get_client):
        """Verify chat API successfully calls Gemini API and returns generated reply."""
        # Create a mock Gemini Client and Response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Here is an explanation of Python lists with real AI!"
        mock_client.models.generate_content.return_value = mock_response
        mock_get_client.return_value = mock_client

        response = self.client.post(
            "/api/chat",
            data=json.dumps({"message": "Explain Python lists"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data.get("status"), "success")
        self.assertEqual(data.get("reply"), "Here is an explanation of Python lists with real AI!")
        self.assertIn("timestamp", data)
        mock_client.models.generate_content.assert_called_once()

    @patch("app.get_gemini_client")
    def test_chat_api_rate_limit_error_handling(self, mock_get_client):
        """Verify chat API handles RESOURCE_EXHAUSTED / rate limit errors gracefully."""
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("429 RESOURCE_EXHAUSTED: quota exceeded")
        mock_get_client.return_value = mock_client

        response = self.client.post(
            "/api/chat",
            data=json.dumps({"message": "Tell me a story"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data.get("status"), "success")
        self.assertIn("Rate Limit Reached", data.get("reply", ""))

    def test_chat_api_empty_message_validation(self):
        """Verify empty or whitespace message returns status 400 with helpful error."""
        response = self.client.post(
            "/api/chat",
            data=json.dumps({"message": "   "}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data.get("status"), "error")

if __name__ == "__main__":
    unittest.main()

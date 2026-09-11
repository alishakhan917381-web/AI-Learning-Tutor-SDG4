# 🤖 CampusBot - AI College Chatbot Website (Powered by Google Gemini AI)

A modern, responsive, and beginner-friendly AI Chatbot web application designed for college mini-projects, demonstrations, and practical exams.

Built using **HTML5, CSS3, JavaScript (ES6)**, **Python Flask**, and the **Google Gemini API** (`google-genai` SDK).

---

## 🌟 Key Features

- 🧠 **Real Google Gemini AI Integration**: Live natural language answers generated directly via the Google Gemini API (default: `gemini-2.5-flash`).
- 🔐 **Secure Environment Variable Handling**: API keys are securely loaded from a local `.env` file and **never hard-coded** into source files.
- 💬 **Interactive Chat Interface**: Realistic conversational speech bubbles with timestamps, user & bot avatars, and markdown formatting (bolding, lists, links, syntax-styled code blocks).
- ⚡ **Loading / Typing Indicator**: Animated 3-dot thinking indicator displayed while awaiting responses from Gemini.
- 🧹 **Clear Chat Button**: Resets conversation history with a single click and confirmation prompt.
- 🚀 **Quick Suggestion Chips**: One-tap query buttons (Admissions, Courses, Exams, Placements, Python Help, Jokes) for effortless project demos.
- 📱 **Fully Responsive Design**: Fluid layout that adapts smoothly across desktops, laptops, tablets, and smartphones.
- 🛡️ **Robust Error Handling**: Graceful fallback notices when the API key is missing or when rate limits / connection issues occur.

---

## 📁 Project Directory Structure

```text
AI-Chatbot/
├── .env.example             # Example environment variable template
├── .gitignore               # Excludes .env and cache from git
├── app.py                   # Flask server & Google Gemini API integration
├── requirements.txt         # Project Python dependencies (Flask, google-genai, python-dotenv)
├── run.bat                  # One-click startup script for Windows
├── README.md                # Project documentation and viva guide
├── test_app.py              # Automated test suite
├── templates/
│   └── index.html           # Main HTML5 web interface
└── static/
    ├── css/
    │   └── style.css        # Responsive CSS styling, code blocks & animations
    └── js/
        └── script.js        # Chat controller, markdown parser & API fetch calls
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **AI Model** | Google Gemini (`gemini-2.5-flash`) | Natural language understanding and response generation |
| **Backend** | Python 3 & Flask | REST API (`/api/chat`), environment config, GenAI client |
| **Environment** | `python-dotenv` | Loads sensitive variables from `.env` securely |
| **Frontend** | HTML5 & CSS3 | Semantic markup and modern, responsive glassmorphism UI |
| **Scripting** | JavaScript (ES6) | Client-side controller, async `fetch()`, code rendering |

---

## 🔑 Setup & Configuration (Gemini API Key)

1. **Get a free Gemini API key**:
   - Visit [Google AI Studio](https://aistudio.google.com/).
   - Sign in with your Google account and click **"Create API Key"**.
   - Copy your generated API key.

2. **Create your `.env` file**:
   - In the `AI-Chatbot` folder, make a copy of `.env.example` and name it `.env`:
     ```bash
     copy .env.example .env
     ```
   - Open `.env` and paste your key:
     ```env
     GEMINI_API_KEY=AIzaSyYourActualKeyHere
     GEMINI_MODEL=gemini-2.5-flash
     PORT=5000
     ```

> **Security Note**: Never commit or share your `.env` file. The `.gitignore` file already prevents it from being tracked in git.

---

## 🚀 How to Run the Project

### Option 1: One-Click Startup (Windows)
Double-click the [`run.bat`](file:///c:/Users/ALISHA%20KHAN/OneDrive/Desktop/AI-Chatbot/run.bat) file inside the `AI-Chatbot` folder.

### Option 2: Command Line (PowerShell / Command Prompt)
1. Open terminal inside the project folder:
   ```powershell
   cd "C:\Users\ALISHA KHAN\OneDrive\Desktop\AI-Chatbot"
   ```
2. Start the application:
   ```powershell
   C:\ProgramData\anaconda3\python.exe app.py
   ```
3. Open your web browser and navigate to:
   ```text
   http://127.0.0.1:5000
   ```

---

## 🧪 Testing

To run the automated test suite and check for errors:
```powershell
C:\ProgramData\anaconda3\python.exe test_app.py
```

---

## 🎓 College Viva & Project Defense Q&A

### 1. Why use an environment variable instead of hard-coding the API key?
> Hard-coding API keys in source code is a major security hazard. If code is pushed to GitHub or shared, anyone can steal the key and exhaust the quota. Using environment variables via `.env` keeps secrets separate from code, and `.gitignore` ensures the key is never accidentally committed.

### 2. What SDK is used to interact with Gemini?
> We use the official `google-genai` SDK (`google.genai.Client`). It supports the latest Gemini models such as `gemini-2.5-flash` with system instructions, temperature control, and high performance.

### 3. How does the frontend communicate with the backend?
> The frontend uses JavaScript's `fetch()` to send an asynchronous `POST` request with a JSON payload (`{ "message": "..." }`) to the Flask `/api/chat` route. The server forwards the prompt to Gemini and returns the AI reply to the browser without refreshing the page.

### 4. How are code snippets and formatting handled in the UI?
> When Gemini returns code blocks (e.g. ````python ... ````) or markdown formatting, the client-side JavaScript parses them into syntax-highlighted code containers, bold text, headings, and clean list elements.

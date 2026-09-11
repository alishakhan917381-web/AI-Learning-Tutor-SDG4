document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("chat-form");
    const input = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    const chatBox = document.getElementById("chat-box");

    const typing = document.getElementById(
        "typing-indicator"
    );

    const clearBtn = document.getElementById(
        "clear-chat-btn"
    );

    const levelSelect = document.getElementById(
        "learner-level"
    );

    const modeSelect = document.getElementById(
        "learning-mode"
    );

    const actionButtons =
        document.querySelectorAll(".action-btn");


    // --------------------------------------------------
    // Time
    // --------------------------------------------------

    function getTime() {

        return new Date().toLocaleTimeString(
            [],
            {
                hour: "2-digit",
                minute: "2-digit"
            }
        );
    }


    // --------------------------------------------------
    // Escape HTML
    // --------------------------------------------------

    function escapeHTML(text) {

        const div = document.createElement("div");

        div.textContent = text;

        return div.innerHTML;
    }


    // --------------------------------------------------
    // Format AI response
    // --------------------------------------------------

    function formatResponse(text) {

        if (!text) {
            return "";
        }

        let safe = escapeHTML(text);

        // Code blocks
        safe = safe.replace(
            /```([\s\S]*?)```/g,
            function(match, code) {

                return `
                    <pre class="code-block">
${code.trim()}
                    </pre>
                `;
            }
        );

        // Bold
        safe = safe.replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        );

        // Headings
        safe = safe.replace(
            /^### (.*)$/gm,
            "<h4>$1</h4>"
        );

        safe = safe.replace(
            /^## (.*)$/gm,
            "<h3>$1</h3>"
        );

        // Bullet points
        safe = safe.replace(
            /^[•*-]\s+(.*)$/gm,
            "<div class='bullet'>• $1</div>"
        );

        // New lines
        safe = safe.replace(
            /\n/g,
            "<br>"
        );

        return safe;
    }


    // --------------------------------------------------
    // Add message
    // --------------------------------------------------

    function addMessage(
        sender,
        message,
        time = null
    ) {

        const group =
            document.createElement("div");

        group.className =
            "message-group " + sender;


        const avatar =
            sender === "user"
                ? "👨‍🎓"
                : "🤖";


        const content =
            sender === "user"
                ? escapeHTML(message)
                : formatResponse(message);


        group.innerHTML = `

            <div class="avatar">
                ${avatar}
            </div>

            <div class="message-content">

                <div class="message-bubble">
                    ${content}
                </div>

                <span class="message-time">
                    ${time || getTime()}
                </span>

            </div>

        `;

        chatBox.appendChild(group);

        scrollBottom();
    }


    // --------------------------------------------------
    // Scroll
    // --------------------------------------------------

    function scrollBottom() {

        setTimeout(() => {

            chatBox.scrollTop =
                chatBox.scrollHeight;

        }, 50);
    }


    // --------------------------------------------------
    // Typing
    // --------------------------------------------------

    function showTyping() {

        typing.classList.remove(
            "hidden"
        );

        scrollBottom();
    }


    function hideTyping() {

        typing.classList.add(
            "hidden"
        );
    }


    // --------------------------------------------------
    // Send message
    // --------------------------------------------------

    async function sendMessage(
        message,
        selectedMode = null
    ) {

        const text = message.trim();

        if (!text) {
            return;
        }


        const level =
            levelSelect.value;


        const mode =
            selectedMode ||
            modeSelect.value;


        addMessage(
            "user",
            text
        );


        input.value = "";

        input.disabled = true;

        sendBtn.disabled = true;


        showTyping();


        try {

            const response =
                await fetch(
                    "/api/chat",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            message: text,
                            level: level,
                            mode: mode
                        })
                    }
                );


            const data =
                await response.json();


            hideTyping();


            if (
                data.status === "success"
            ) {

                addMessage(
                    "bot",
                    data.reply,
                    data.timestamp
                );

            } else {

                addMessage(
                    "bot",
                    "⚠️ " +
                    (data.message ||
                     "Something went wrong.")
                );
            }


        } catch (error) {

            console.error(
                "Chat error:",
                error
            );


            hideTyping();


            addMessage(
                "bot",
                "⚠️ **Connection Error**\n\n" +
                "Please make sure the Flask server is running."
            );

        } finally {

            input.disabled = false;

            sendBtn.disabled = false;

            input.focus();
        }
    }


    // --------------------------------------------------
    // Form submit
    // --------------------------------------------------

    form.addEventListener(
        "submit",
        function(event) {

            event.preventDefault();

            sendMessage(
                input.value
            );

        }
    );


    // --------------------------------------------------
    // Quick action buttons
    // --------------------------------------------------

    actionButtons.forEach(
        button => {

            button.addEventListener(
                "click",
                () => {

                    const query =
                        button.dataset.query;

                    const mode =
                        button.dataset.mode;

                    modeSelect.value =
                        mode;

                    sendMessage(
                        query,
                        mode
                    );
                }
            );
        }
    );


    // --------------------------------------------------
    // Clear chat
    // --------------------------------------------------

    clearBtn.addEventListener(
        "click",
        () => {

            chatBox.innerHTML = `

                <div class="message-group bot">

                    <div class="avatar">
                        🤖
                    </div>

                    <div class="message-content">

                        <div class="message-bubble">

                            <h3>
                                👋 Chat cleared!
                            </h3>

                            <p>
                                What would you like
                                to learn today?
                            </p>

                        </div>

                        <span class="message-time">
                            ${getTime()}
                        </span>

                    </div>

                </div>

            `;

            input.focus();
        }
    );


    input.focus();

});
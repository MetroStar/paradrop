import { MODEL_URL } from './config.min.js'

document.addEventListener("DOMContentLoaded", function () {
  const chatContainer = document.getElementById("chatContainer");
  const chatInput = document.getElementById("chatInput");
  const sendButton = document.getElementById("sendMessage");
  const clearInputButton = document.getElementById("clearInput");
  const clearChatButton = document.getElementById("clearChat");
  const copyChatButton = document.getElementById("copyChat");
  const notificationBar = document.getElementById("notificationBar");

  function showNotification(message) {
    notificationBar.textContent = message;
    notificationBar.style.display = "block";
    setTimeout(() => {
      notificationBar.style.display = "none";
    }, 3000);
  }

  function addMessage(content, isUser = true) {
    const messageGroup = document.createElement("div");
    messageGroup.classList.add(
      "message-group",
      isUser ? "user-group" : "system-group"
    );

    const label = document.createElement("div");
    label.classList.add("message-label");
    label.textContent = isUser ? "You" : "Paradrop AI";

    const messageElement = document.createElement("div");
    messageElement.classList.add(
      "chat-message",
      isUser ? "user-message" : "system-message"
    );

    const copyButton = document.createElement("button");
    copyButton.classList.add("copy-button");
    copyButton.textContent = "📋";
    copyButton.setAttribute("aria-label", "Copy message");
    copyButton.addEventListener("click", function () {
      navigator.clipboard.writeText(content).then(
        function () {
          showNotification("Message copied to clipboard!");
        },
        function (err) {
          console.error("Could not copy text: ", err);
        }
      );
    });

    messageElement.appendChild(copyButton);

    const codeRegex = /```(\w+)?\s*([\s\S]*?)```/g;
    let lastIndex = 0;
    let match;

    while ((match = codeRegex.exec(content)) !== null) {
      if (match.index > lastIndex) {
        messageElement.appendChild(
          document.createTextNode(content.slice(lastIndex, match.index))
        );
      }

      const pre = document.createElement("pre");
      const code = document.createElement("code");
      if (match[1]) {
        code.className = `language-${match[1]}`;
      }
      code.textContent = match[2].trim();
      pre.appendChild(code);
      messageElement.appendChild(pre);

      lastIndex = match.index + match[0].length;
    }

    if (lastIndex < content.length) {
      messageElement.appendChild(
        document.createTextNode(content.slice(lastIndex))
      );
    }

    messageGroup.appendChild(label);
    messageGroup.appendChild(messageElement);

    chatContainer.appendChild(messageGroup);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  function addThinkingMessage() {
    const messageGroup = document.createElement("div");
    messageGroup.classList.add("message-group", "system-group");

    const label = document.createElement("div");
    label.classList.add("message-label");
    label.textContent = "Paradrop AI";

    const messageElement = document.createElement("div");
    messageElement.classList.add("chat-message", "system-message");

    const thinkingIndicator = document.createElement("div");
    thinkingIndicator.classList.add("thinking");

    const thinkingText = document.createTextNode("Thinking...");

    messageElement.appendChild(thinkingIndicator);
    messageElement.appendChild(thinkingText);

    messageGroup.appendChild(label);
    messageGroup.appendChild(messageElement);

    chatContainer.appendChild(messageGroup);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    return messageGroup;
  }

  clearInputButton.addEventListener("click", function () {
    chatInput.value = "";
  });

  clearChatButton.addEventListener("click", function () {
    chatContainer.innerHTML = "";
  });

  copyChatButton.addEventListener("click", function () {
    const chatText = Array.from(
      chatContainer.querySelectorAll(".message-group")
    )
      .map((group) => {
        const label = group.querySelector(".message-label").textContent;
        const messageElement = group.querySelector(".chat-message");
        const message = Array.from(messageElement.childNodes)
          .filter(
            (node) =>
              node.nodeType === Node.TEXT_NODE || node.nodeName !== "BUTTON"
          )
          .map((node) => node.textContent.trim())
          .join("");
        return `${label}: ${message}`;
      })
      .join("\n\n");
    navigator.clipboard.writeText(chatText).then(
      function () {
        showNotification("Chat Copied to Clipboard!");
      },
      function (err) {
        console.error("Could Not Copy Text: ", err);
      }
    );
  });

  sendButton.addEventListener("click", function () {
    const message = chatInput.value.trim();
    if (message) {
      addMessage(message, true);

      chatInput.value = "";
      const thinkingMessage = addThinkingMessage();
      setTimeout(() => {
        chatContainer.removeChild(thinkingMessage);
      }, 18000);

      const apiUrl =
        `${MODEL_URL}` +
        encodeURIComponent(message);

      fetch(apiUrl, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP ERROR Status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          addMessage(data.answer, false);
        })
        .catch((error) => {
          console.error("Fetch Error:", error);
          const thinkingMessage = addThinkingMessage();
          setTimeout(() => {
            chatContainer.removeChild(thinkingMessage);
            addMessage("Error Model Might Not Be Running", false);
          }, 2000);
        });
    }
  });

  chatInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendButton.click();
    }
  });

  document.querySelectorAll(".copy-button").forEach((button) => {
    button.addEventListener("click", function () {
      const messageText = this.nextSibling.textContent.trim();
      navigator.clipboard.writeText(messageText).then(
        function () {
          showNotification("Message copied to clipboard!");
        },
        function (err) {
          console.error("Could not copy text: ", err);
        }
      );
    });
  });
});

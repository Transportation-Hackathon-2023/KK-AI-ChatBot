document.addEventListener("DOMContentLoaded", function() {
  const sendButton = document.getElementById("send-button");
  const userInput = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");

  sendButton.addEventListener("click", function() {
    const userText = userInput.value;
    chatBox.innerHTML += `<p>User: ${userText}</p>`;

    // TODO: Send `userText` to your Flask backend and get a response

    userInput.value = "";
  });
});

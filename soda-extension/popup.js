document.getElementById("scrape-btn").addEventListener("click", async () => {
  // Execute content.js in the current tab
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ["content.js"],
  });
});

chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
  try {
    console.log("message", JSON.stringify(message.URL.location.href));

    response = await fetch("http://localhost:5000/summarize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        policyURL: message.URL.location.href,
      }),
    });
    // console.log("Response from ChatGPT:", response.json());
    document.getElementById("chatGptRes").innerText = (
      await response.json()
    ).summary;
  } catch (error) {
    console.error("Error:", error);
  }
});

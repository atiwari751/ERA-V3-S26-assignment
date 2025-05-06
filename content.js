// content.js

console.log("[Content Script] Injected into:", window.location.href);

// Since we are injecting at document_start, the DOM may not be ready,
// so check if we need to wait until later:
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => {
    console.log("[Content Script] DOMContentLoaded fired");
    sendPageData();
  });
} else {
  console.log("[Content Script] Document already loaded");
  sendPageData();
}

function sendPageData() {
  // A small delay can be used if necessary.
  setTimeout(() => {
    const pageText = document.body && document.body.innerText ? document.body.innerText : "";
    console.log("[Content Script] Sending page data to background:", window.location.href);
    chrome.runtime.sendMessage({
      action: "pageContent",
      url: window.location.href,
      text: pageText
    });
  }, 500);
}

// Listen for messages from the background script to highlight text.
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === "highlight" && message.query) {
    highlightText(message.query);
  }
});

/**
 * Highlights all occurrences of the provided query text on the page.
 *
 * WARNING: Replacing innerHTML may disrupt some pages.
 *
 * @param {string} query - The text to highlight.
 */
function highlightText(query) {
  if (!query) return;
  // Escape any special regex characters in the query.
  const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(escapedQuery, 'gi');
  document.body.innerHTML = document.body.innerHTML.replace(regex, function(match) {
    return '<span style="background-color: yellow;">' + match + '</span>';
  });
}

// content.js

// When the DOM is loaded, send the page text and URL to the background for indexing.
document.addEventListener("DOMContentLoaded", function() {
  // Delay a little to ensure most of the page has loaded.
  setTimeout(() => {
    const pageText = document.body.innerText;
    chrome.runtime.sendMessage({
      action: "pageContent",
      url: window.location.href,
      text: pageText
    });
  }, 1000);
});

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

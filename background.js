// background.js

// Set the base URL for your FastAPI backend.
const FASTAPI_BASE_URL = "http://localhost:8000";

// Listen for messages from content and popup scripts.
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === "pageContent") {
        // Message from content.js: index the current page.
        // msg should contain: { url, text }
        indexPageViaBackend(msg.url, msg.text);
    } else if (msg.action === "retrieve") {
        // Message from popup.js: retrieve pages similar to the query.
        // msg should contain: { query }
        retrievePagesViaBackend(msg.query)
            .then(results => {
                sendResponse({ results: results });
            })
            .catch(err => {
                console.error("Error retrieving pages:", err);
                sendResponse({ results: [] });
            });
        // Return true to keep the messaging channel open for asynchronous response.
        return true;
    } else if (msg.action === "openAndHighlight") {
        // Message from popup.js: open page and highlight query text.
        // msg should contain: { result, query }
        openAndHighlight(msg.result.url, msg.query);
    }
});

// Sends the page information to the FastAPI backend for indexing.
function indexPageViaBackend(url, text) {
    fetch(`${FASTAPI_BASE_URL}/index`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url, text: text })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Indexed page with ID:", data.id);
    })
    .catch(err => {
        console.error("Error indexing page:", err);
    });
}

// Sends the user query to the FastAPI backend for retrieval.
async function retrievePagesViaBackend(query) {
    try {
        const response = await fetch(`${FASTAPI_BASE_URL}/query`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: query })
        });
        if (!response.ok) {
            throw new Error("Failed to retrieve pages");
        }
        const data = await response.json();
        // data.results is expected to be an array of page metadata.
        return data.results;
    } catch (error) {
        console.error("Error in retrieval:", error);
        return [];
    }
}

// Opens a new tab with the target URL and instructs the content script to highlight the query text.
function openAndHighlight(url, query) {
    chrome.tabs.create({ url: url }, function(tab) {
        chrome.tabs.onUpdated.addListener(function listener(tabId, changeInfo) {
            if (tabId === tab.id && changeInfo.status === "complete") {
                chrome.tabs.sendMessage(tab.id, { action: "highlight", query: query });
                chrome.tabs.onUpdated.removeListener(listener);
            }
        });
    });
}

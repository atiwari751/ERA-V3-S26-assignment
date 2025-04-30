document.getElementById("search-btn").addEventListener("click", function() {
  const query = document.getElementById("query-input").value.trim();
  if (!query) {
    alert("Please enter a search query.");
    return;
  }

  // Send the query to the background script for retrieval.
  chrome.runtime.sendMessage({ action: "retrieve", query: query }, function(response) {
    const results = response.results;
    displayResults(results, query);
  });
});

/**
 * Displays the search results in the popup.
 *
 * @param {Array} results - Array of page objects.
 * @param {string} query - The search query.
 */
function displayResults(results, query) {
  const resultsContainer = document.getElementById("results");
  resultsContainer.innerHTML = "";

  if (results.length === 0) {
    resultsContainer.innerHTML = "<p>No matching pages found.</p>";
    return;
  }

  results.forEach(result => {
    const div = document.createElement("div");
    div.className = "result-item";
    div.textContent = result.url;
    div.addEventListener("click", () => {
      // Tell the background to open the page and highlight the query.
      chrome.runtime.sendMessage({
        action: "openAndHighlight",
        result: result,
        query: query
      });
    });
    resultsContainer.appendChild(div);
  });
}

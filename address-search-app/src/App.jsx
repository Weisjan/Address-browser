import { useState } from "react";
import SearchBar from "./components/SearchBar";
import ResultsList from "./components/ResultsList";

export default function App() {
  const [searchResults, setSearchResults] = useState({ results: [], type: "" });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (query, searchType) => {
    if (query.length < 2) return;

    setIsLoading(true);
    setError(null);

    try {
      const endpointMap = {
        street: "streets",
        locality: "localities",
        commune: "communes",
        county: "counties",
      };

      const endpoint = endpointMap[searchType];
      const response = await fetch(
        `http://127.0.0.1:8000/search/${endpoint}?query=${encodeURIComponent(
          query
        )}`
      );

      if (!response.ok) {
        throw new Error(`Search failed with status: ${response.status}`);
      }

      const data = await response.json();
      setSearchResults(data);
    } catch (err) {
      setError(err.message);
      setSearchResults({ results: [], type: "" });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Address Search</h1>
      <SearchBar onSearch={handleSearch} />

      {isLoading && <div className="loading">Loading results...</div>}
      {error && <div className="error">Error: {error}</div>}
      {!isLoading && !error && (
        <ResultsList
          results={searchResults.results}
          type={searchResults.type}
        />
      )}
    </div>
  );
}

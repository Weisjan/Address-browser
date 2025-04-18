import { useState } from "react";
import SearchBar from "./components/SearchBar";
import ResultsList from "./components/ResultsList";

export default function App() {
  const [searchResults, setSearchResults] = useState({ results: [], type: "" });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const resultsPerPage = 5;

  const handleSearch = async (query, searchType) => {
    if (query.length < 2) return;

    setIsLoading(true);
    setError(null);
    setCurrentPage(1);

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

  const indexOfLastResult = currentPage * resultsPerPage;
  const indexOfFirstResult = indexOfLastResult - resultsPerPage;
  const currentResults = searchResults.results.slice(
    indexOfFirstResult,
    indexOfLastResult
  );
  const totalPages = Math.ceil(searchResults.results.length / resultsPerPage);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  return (
    <div className="min-h-screen bg-[aliceblue] font-montserrat p-10">
      <div className="font-montserrat max-w-[800px] mx-auto bg-white p-8 rounded-[10px] shadow-md">
        <h1 className="text-2xl font-bold mb-6">Address Search</h1>
        <SearchBar onSearch={handleSearch} />
        {isLoading && (
          <div className="mt-6 text-gray-600">Loading results...</div>
        )}
        {error && <div className="mt-6 text-red-500">Error: {error}</div>}
        {!isLoading && !error && (
          <ResultsList
            results={currentResults}
            type={searchResults.type}
            currentPage={currentPage}
            totalPages={totalPages}
            totalResults={searchResults.results.length}
            onPageChange={handlePageChange}
          />
        )}
      </div>
    </div>
  );
}

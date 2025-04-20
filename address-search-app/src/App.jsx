import { useState } from "react";
import SearchBar from "./components/SearchBar";
import ResultsList from "./components/ResultsList";
import BrowseAddress from "./components/BrowseAddress.jsx";

export default function App() {
  const [searchResults, setSearchResults] = useState({ results: [], type: "" });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [activeTab, setActiveTab] = useState("search");
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
    <div className="min-h-screen bg-[aliceblue] font-['Montserrat',_Arial,_sans-serif] py-10 px-5 m-0">
      <div className="max-w-[750px] mx-auto bg-white p-8 rounded-[10px] shadow-md">
        <h1 className="text-2xl font-bold mb-6">Address Search</h1>

        <div className="flex mb-6 border-b">
          <button
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === "search"
                ? "text-[#608abf] border-b-2 border-[#608abf]"
                : "text-gray-500 hover:text-gray-700"
            }`}
            onClick={() => setActiveTab("search")}
          >
            Search
          </button>
          <button
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === "browse"
                ? "text-[#608abf] border-b-2 border-[#608abf]"
                : "text-gray-500 hover:text-gray-700"
            }`}
            onClick={() => setActiveTab("browse")}
          >
            Browse
          </button>
        </div>

        {activeTab === "search" && (
          <>
            <SearchBar onSearch={handleSearch} />
            {isLoading && (
              <div className="mt-6 flex items-center gap-2 text-gray-600">
                <div className="w-5 h-5 border-2 border-t-transparent border-[#608abf] rounded-full animate-spin"></div>
                <span>Loading results...</span>
              </div>
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
          </>
        )}

        {activeTab === "browse" && <BrowseAddress />}
      </div>
    </div>
  );
}

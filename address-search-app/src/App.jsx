import { useState } from "react";
import SearchBar from "./components/SearchBar";
import ResultsList from "./components/ResultsList";

export default function App() {
  const [results, setResults] = useState([]);
  const [resultType, setResultType] = useState("");

  const handleSearch = async (query, type) => {
    if (query.length < 2) return;

    const res = await fetch(
      `http://localhost:8000/szukaj?q=${encodeURIComponent(query)}&typ=${type}`
    );
    const data = await res.json();

    setResults(data.wyniki);
    setResultType(data.typ);
  };

  return (
    <div className="container">
      <h1>🔍 Wyszukiwarka Adresów</h1>
      <SearchBar onSearch={handleSearch} />
      <ResultsList results={results} type={resultType} />
    </div>
  );
}

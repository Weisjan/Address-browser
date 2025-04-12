import { useState } from "react";
import SearchBar from "./components/SearchBar";
import ResultsList from "./components/ResultsList";

export default function App() {
  const [data, setData] = useState({ wyniki: [], typ: "" });

  const handleSearch = async (q, t) => {
    if (q.length < 2) return;

    const res = await fetch(`http://localhost:8000/szukaj?q=${q}&typ=${t}`);
    setData(await res.json());
  };

  return (
    <div className="container">
      <h1>Wyszukiwarka Adresów</h1>
      <SearchBar onSearch={handleSearch} />
      <ResultsList results={data.wyniki} type={data.typ} />
    </div>
  );
}

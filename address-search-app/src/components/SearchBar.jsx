import { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Wpisz miejscowość lub ulicę..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button type="submit">Szukaj</button>
    </form>
  );
}

import { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [query, setQuery] = useState("");
  const [type, setType] = useState("miejscowosc");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query, type);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        class="search-input"
        type="text"
        placeholder="Wpisz zapytanie..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <div class="radio-group">
        {["ulica", "miejscowosc", "gmina", "powiat"].map((value) => (
          <label
            key={value}
            class={`radio-option ${type === value ? "active" : ""}`}
          >
            <input
              type="radio"
              value={value}
              checked={type === value}
              onChange={(e) => setType(e.target.value)}
            />
            {value.charAt(0).toUpperCase() + value.slice(1)}
          </label>
        ))}
      </div>

      <button type="submit">Szukaj</button>
    </form>
  );
}

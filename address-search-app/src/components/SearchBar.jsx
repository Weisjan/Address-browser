import { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [query, setQuery] = useState("");
  const [type, setType] = useState("locality");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query, type);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        className="search-input"
        type="text"
        placeholder="Enter your query"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <div className="radio-group">
        {["street", "locality", "commune", "county"].map((value) => (
          <label
            key={value}
            className={`radio-option ${type === value ? "active" : ""}`}
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

      <button className="searchbutton" type="submit">
        Search
      </button>
    </form>
  );
}

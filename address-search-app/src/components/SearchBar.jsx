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
        className="w-full px-4 py-3 text-base border-2 border-gray-200 rounded-lg outline-none focus:border-[#608abf] transition-colors shadow-sm"
        type="text"
        placeholder="Enter your query"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <div className="flex flex-wrap gap-3 my-5">
        {["street", "locality", "commune", "county"].map((value) => (
          <label
            key={value}
            className={`px-5 py-2 border-2 rounded-full cursor-pointer select-none text-sm transition-all ${
              type === value
                ? "bg-[#608abf] text-white border-[#608abf]"
                : "bg-[#f3f4f6] text-gray-700 border-gray-300 hover:border-[#608abf] hover:text-[#608abf]"
            }`}
          >
            <input
              type="radio"
              value={value}
              checked={type === value}
              onChange={(e) => setType(e.target.value)}
              className="hidden"
            />
            {value.charAt(0).toUpperCase() + value.slice(1)}
          </label>
        ))}
      </div>

      <button
        className="px-6 py-3 text-base bg-[#608abf] cursor-pointer text-white border-none rounded-lg mt-2 hover:shadow-md transition-shadow"
        type="submit"
      >
        Search
      </button>
    </form>
  );
}

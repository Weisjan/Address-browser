import { useState, useEffect } from "react";

export default function BrowseAddress() {
  const [hierarchy, setHierarchy] = useState([]);
  const [currentLevel, setCurrentLevel] = useState("voivodeship");
  const [items, setItems] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async (level, parentId = null) => {
    setIsLoading(true);
    setError(null);

    try {
      let url = `http://127.0.0.1:8000/browse/${level}`;

      if (parentId) {
        const parentParam = getParentParamForLevel(level);
        url += `?${parentParam}=${parentId}`;
      }

      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(
          `Failed to fetch ${level} with status: ${response.status}`
        );
      }

      const data = await response.json();
      setItems(data.items);
    } catch (err) {
      setError(err.message);
      setItems([]);
    } finally {
      setIsLoading(false);
    }
  };

  const getParentParamForLevel = (level) => {
    switch (level) {
      case "county":
        return "voivodeship_id";
      case "commune":
        return "county_id";
      case "locality":
        return "commune_id";
      case "street":
        return "locality_id";
      case "address":
        return "street_id";
      default:
        return "";
    }
  };

  const handleItemSelect = (item) => {
    const newHierarchy = [...hierarchy, item];
    setHierarchy(newHierarchy);

    const nextLevel = getNextLevel(currentLevel);

    fetchData(nextLevel, item.id);

    setCurrentLevel(nextLevel);
  };

  const getNextLevel = (level) => {
    const levels = [
      "voivodeship",
      "county",
      "commune",
      "locality",
      "street",
      "address",
    ];
    const currentIndex = levels.indexOf(level);

    if (currentIndex < levels.length - 1) {
      return levels[currentIndex + 1];
    }

    return level;
  };

  const handleNavigateBack = (index) => {
    if (index < 0) return;

    const newHierarchy = hierarchy.slice(0, index + 1);
    setHierarchy(newHierarchy);

    const levels = [
      "voivodeship",
      "county",
      "commune",
      "locality",
      "street",
      "address",
    ];
    const newLevel = index < 0 ? "voivodeship" : levels[index + 1];
    setCurrentLevel(newLevel);

    if (index < 0) {
      fetchData("voivodeship");
    } else {
      fetchData(newLevel, newHierarchy[index].id);
    }
  };

  useEffect(() => {
    fetchData("voivodeship");
  }, []);

  const getLevelTitle = () => {
    const titles = {
      voivodeship: "Voivodeships",
      county: "Counties",
      commune: "Communes",
      locality: "Localities",
      street: "Streets",
      address: "Addresses",
    };

    return titles[currentLevel] || "";
  };

  const renderItemContent = (item) => {
    if (currentLevel === "address") {
      return (
        <>
          <p className="font-medium">
            {item.number} {hierarchy[hierarchy.length - 1]?.name}
          </p>
          {item.postal_code && (
            <p className="text-sm text-gray-600 mt-1">{item.postal_code}</p>
          )}
        </>
      );
    }

    return (
      <>
        <p className="font-medium">{item.name}</p>
        {item.info && <p className="text-sm text-gray-600 mt-1">{item.info}</p>}
      </>
    );
  };

  return (
    <div className="mt-8">
      <div className="flex flex-wrap items-center gap-2 mb-6">
        <button
          onClick={() => {
            setHierarchy([]);
            setCurrentLevel("voivodeship");
            fetchData("voivodeship");
          }}
          className="text-blue-600 hover:underline font-medium"
        >
          Home
        </button>

        {hierarchy.map((item, index) => (
          <div key={index} className="flex items-center">
            <span className="mx-2 text-gray-400">/</span>
            <button
              onClick={() => handleNavigateBack(index - 1)}
              className="text-blue-600 hover:underline font-medium"
            >
              {item.name}
            </button>
          </div>
        ))}
      </div>

      <h3 className="text-xl font-semibold mb-4">{getLevelTitle()}</h3>

      {isLoading && <div className="p-4 text-gray-600">Loading...</div>}

      {error && <div className="p-4 text-red-500">Error: {error}</div>}

      {!isLoading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {items.map((item) => (
            <div
              key={item.id}
              className={`p-4 bg-gray-50 rounded-lg border border-gray-200 ${
                currentLevel !== "address"
                  ? "hover:bg-gray-100 hover:border-gray-300"
                  : ""
              } transition-colors text-left`}
            >
              {currentLevel !== "address" ? (
                <button
                  className="w-full text-left"
                  onClick={() => handleItemSelect(item)}
                >
                  {renderItemContent(item)}
                </button>
              ) : (
                renderItemContent(item)
              )}

              {currentLevel === "address" && (
                <div className="mt-2 pt-2 border-t border-gray-200">
                  <p className="text-sm">
                    <span className="font-medium">Full address:</span>{" "}
                    {item.number} {hierarchy[hierarchy.length - 1]?.name},{" "}
                    {hierarchy[hierarchy.length - 2]?.name}
                    {item.postal_code && `, ${item.postal_code}`}
                  </p>
                </div>
              )}
            </div>
          ))}

          {items.length === 0 && !isLoading && (
            <div className="col-span-3 p-4 text-gray-600">
              No items found at this level.
            </div>
          )}
        </div>
      )}
    </div>
  );
}

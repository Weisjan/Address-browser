export default function ResultsList({
  results,
  type,
  currentPage,
  totalPages,
  totalResults,
  onPageChange,
}) {
  if (!results || results.length === 0) {
    return <p className="mt-6">No results.</p>;
  }

  const startResult = (currentPage - 1) * 5 + 1;
  const endResult = Math.min(currentPage * 5, totalResults);

  const renderPageButton = (pageNumber) => (
    <button
      key={pageNumber}
      onClick={() => onPageChange(pageNumber)}
      className={`px-4 py-2 border-2 rounded-full cursor-pointer select-none text-sm transition-all ${
        currentPage === pageNumber
          ? "bg-[#608abf] text-white border-[#608abf]"
          : "bg-gray-100 text-gray-700 border-gray-300 hover:border-[#608abf] hover:text-[#608abf]"
      }`}
    >
      {pageNumber}
    </button>
  );

  const renderEllipsis = (key) => (
    <span key={`ellipsis-${key}`} className="mx-1 font-bold">
      ...
    </span>
  );

  const renderPageRange = (start, end) => {
    const buttons = [];
    for (let i = start; i <= end; i++) {
      buttons.push(renderPageButton(i));
    }
    return buttons;
  };

  const renderPaginationButtons = () => {
    const buttons = [];

    buttons.push(renderPageButton(1));

    if (totalPages <= 7) {
      buttons.push(...renderPageRange(2, totalPages));
    } else {
      if (currentPage < 5) {
        buttons.push(...renderPageRange(2, 5));
        buttons.push(renderEllipsis(1));
        buttons.push(renderPageButton(totalPages));
      } else if (currentPage > totalPages - 4) {
        buttons.push(renderEllipsis(1));
        buttons.push(...renderPageRange(totalPages - 4, totalPages));
      } else {
        buttons.push(renderEllipsis(1));
        buttons.push(...renderPageRange(currentPage - 1, currentPage + 1));
        buttons.push(renderEllipsis(2));
        buttons.push(renderPageButton(totalPages));
      }
    }

    return buttons;
  };

  const renderResultItem = (item) => {
    switch (type) {
      case "county":
        return (
          <>
            <strong>County:</strong> {item.county} <br />
            <strong>Voivodeship:</strong> {item.voivodeship}
          </>
        );
      case "commune":
        return (
          <>
            <strong>Commune:</strong> {item.commune} <br />
            <strong>County:</strong> {item.county} <br />
            <strong>Voivodeship:</strong> {item.voivodeship}
          </>
        );
      case "locality":
        return (
          <>
            <strong>Locality:</strong> {item.locality} <br />
            <strong>Commune:</strong> {item.commune} <br />
            <strong>County:</strong> {item.county} <br />
            <strong>Voivodeship:</strong> {item.voivodeship}
          </>
        );
      case "street":
        return (
          <>
            <strong>Street:</strong> {item.street} <br />
            <strong>Locality:</strong> {item.locality} <br />
            <strong>Commune:</strong> {item.commune} <br />
            <strong>County:</strong> {item.county} <br />
            <strong>Voivodeship:</strong> {item.voivodeship}
          </>
        );
      default:
        return null;
    }
  };

  return (
    <div className="mt-8">
      <h3 className="text-xl font-semibold mb-4">Results: {type}</h3>

      <div className="text-center text-gray-600 mb-4 text-sm">
        Shown {startResult}-{endResult} from {totalResults} results
      </div>

      <ul className="mt-4 space-y-3">
        {results.map((item, idx) => (
          <li
            key={idx}
            className="p-4 bg-gray-50 rounded-lg border-b border-gray-200 hover:bg-gray-100 transition-colors"
          >
            {renderResultItem(item)}
          </li>
        ))}
      </ul>

      {totalPages > 1 && (
        <div className="flex justify-center mt-6 gap-1">
          <button
            onClick={() => onPageChange(currentPage - 1)}
            disabled={currentPage === 1}
            className={`px-4 py-2 border-2 rounded-full cursor-pointer select-none text-sm transition-all ${
              currentPage === 1
                ? "bg-gray-50 text-gray-300 cursor-not-allowed"
                : "bg-gray-100 text-gray-700 border-gray-300 hover:border-[#608abf] hover:text-[#608abf]"
            }`}
          >
            &laquo; Previous
          </button>

          {renderPaginationButtons()}

          <button
            onClick={() => onPageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
            className={`px-4 py-2 border-2 rounded-full cursor-pointer select-none text-sm transition-all ${
              currentPage === totalPages
                ? "bg-gray-50 text-gray-300 cursor-not-allowed"
                : "bg-gray-100 text-gray-700 border-gray-300 hover:border-[#608abf] hover:text-[#608abf]"
            }`}
          >
            Next &raquo;
          </button>
        </div>
      )}
    </div>
  );
}

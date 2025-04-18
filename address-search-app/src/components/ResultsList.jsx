export default function ResultsList({
  results,
  type,
  currentPage,
  totalPages,
  totalResults,
  onPageChange,
}) {
  if (!results || results.length === 0) {
    return <p>No results.</p>;
  }

  const startResult = (currentPage - 1) * 5 + 1;
  const endResult = Math.min(currentPage * 5, totalResults);

  const renderPageButton = (pageNumber) => (
    <button
      key={pageNumber}
      onClick={() => onPageChange(pageNumber)}
      className={`page-btn ${currentPage === pageNumber ? "active" : ""}`}
    >
      {pageNumber}
    </button>
  );

  const renderEllipsis = (key) => (
    <span key={`ellipsis-${key}`} className="ellipsis">
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
    <div className="results">
      <h3>Results: {type}</h3>

      <div className="results-info">
        Shown {startResult}-{endResult} from {totalResults} results
      </div>

      <ul>
        {results.map((item, idx) => (
          <li key={idx} className="result-item">
            {renderResultItem(item)}
          </li>
        ))}
      </ul>

      {totalPages > 1 && (
        <div className="pagination">
          <button
            onClick={() => onPageChange(currentPage - 1)}
            disabled={currentPage === 1}
            className="page-btn"
          >
            &laquo; Previous
          </button>

          {renderPaginationButtons()}

          <button
            onClick={() => onPageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
            className="page-btn"
          >
            Next &raquo;
          </button>
        </div>
      )}
    </div>
  );
}

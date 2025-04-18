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

  const pageNumbers = [];
  for (let i = 1; i <= totalPages; i++) {
    pageNumbers.push(i);
  }

  const startResult = (currentPage - 1) * 5 + 1;
  const endResult = Math.min(currentPage * 5, totalResults);

  return (
    <div className="results">
      <h3>Results: {type}</h3>

      <div className="results-info">
        Shown {startResult}-{endResult} from {totalResults} results
      </div>

      <ul>
        {results.map((item, idx) => (
          <li key={idx} className="result-item">
            {type === "county" && (
              <>
                <strong>County:</strong> {item.county} <br />
                <strong>Voivodeship:</strong> {item.voivodeship}
              </>
            )}
            {type === "commune" && (
              <>
                <strong>Commune:</strong> {item.commune} <br />
                <strong>County:</strong> {item.county} <br />
                <strong>Voivodeship:</strong> {item.voivodeship}
              </>
            )}
            {type === "locality" && (
              <>
                <strong>Locality:</strong> {item.locality} <br />
                <strong>Commune:</strong> {item.commune} <br />
                <strong>County:</strong> {item.county} <br />
                <strong>Voivodeship:</strong> {item.voivodeship}
              </>
            )}
            {type === "street" && (
              <>
                <strong>Street:</strong> {item.street} <br />
                <strong>Locality:</strong> {item.locality} <br />
                <strong>Commune:</strong> {item.commune} <br />
                <strong>County:</strong> {item.county} <br />
                <strong>Voivodeship:</strong> {item.voivodeship}
              </>
            )}
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

          {pageNumbers.map((number) => (
            <button
              key={number}
              onClick={() => onPageChange(number)}
              className={`page-btn ${currentPage === number ? "active" : ""}`}
            >
              {number}
            </button>
          ))}

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

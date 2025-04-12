export default function ResultsList({ results, type }) {
  if (!results || results.length === 0) {
    return <p>Brak wyników.</p>;
  }

  return (
    <div id="results">
      <h3>Wyniki: {type}</h3>
      <ul>
        {results.map((item, idx) => (
          <li key={idx} className="result-item">
            {type === "powiat" && (
              <>
                <strong>Powiat:</strong> {item.powiat} <br />
                <strong>Województwo:</strong> {item.wojewodztwo}
              </>
            )}
            {type === "gmina" && (
              <>
                <strong>Gmina:</strong> {item.gmina} <br />
                <strong>Powiat:</strong> {item.powiat} <br />
                <strong>Województwo:</strong> {item.wojewodztwo}
              </>
            )}
            {type === "miejscowość" && (
              <>
                <strong>Miejscowość:</strong> {item.miejscowość} <br />
                <strong>Gmina:</strong> {item.gmina} <br />
                <strong>Powiat:</strong> {item.powiat} <br />
                <strong>Województwo:</strong> {item.wojewodztwo}
              </>
            )}
            {type === "ulica" && (
              <>
                <strong>Ulica:</strong> {item.ulica} <br />
                <strong>Miejscowość:</strong> {item.miejscowość} <br />
                <strong>Gmina:</strong> {item.gmina} <br />
                <strong>Powiat:</strong> {item.powiat} <br />
                <strong>Województwo:</strong> {item.wojewodztwo}
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function ResultsList({ results, type }) {
  if (!results || results.length === 0) {
    return <p>Brak wyników.</p>;
  }

  return (
    <div>
      <h3>Wyniki ({type})</h3>
      <ul>
        {results.map((item, idx) => (
          <li key={idx}>
            {type === "miejscowość" && (
              <>
                {item.miejscowosc}, gmina {item.gmina}, powiat {item.powiat},
                woj. {item.wojewodztwo}
              </>
            )}
            {type === "ulica" && (
              <>
                ul. {item.ulica}, {item.miejscowosc}, gmina {item.gmina}, powiat{" "}
                {item.powiat}, woj. {item.wojewodztwo}
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

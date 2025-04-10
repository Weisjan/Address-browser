const apiUrl = "http://localhost:8000/szukaj"; // dostosuj jeśli port/backend inny

async function search() {
  const input = document.getElementById("searchInput").value.trim();
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "";

  if (input.length < 2) {
    resultsDiv.innerHTML = "<p>Wpisz co najmniej 2 znaki.</p>";
    return;
  }

  try {
    const response = await fetch(`${apiUrl}?q=${encodeURIComponent(input)}`);
    const data = await response.json();

    if (data.typ === "brak wyników") {
      resultsDiv.innerHTML = "<p>Brak wyników.</p>";
    } else {
      data.wyniki.forEach((item) => {
        const div = document.createElement("div");
        div.className = "result-item";
        if (data.typ === "miejscowość") {
          div.textContent = `${item.miejscowosc}, gmina: ${item.gmina}, powiat: ${item.powiat}, województwo: ${item.wojewodztwo}`;
        } else if (data.typ === "ulica") {
          div.textContent = `${item.ulica}, ${item.miejscowosc}, gmina: ${item.gmina}, powiat: ${item.powiat}, województwo: ${item.wojewodztwo}`;
        }
        resultsDiv.appendChild(div);
      });
    }
  } catch (err) {
    console.error("Błąd zapytania:", err);
    resultsDiv.innerHTML = "<p>Wystąpił błąd podczas wyszukiwania.</p>";
  }
}

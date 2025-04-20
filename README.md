# Address Browser

Address Browser is a full-stack web application for importing, storing, and querying hierarchical address data from Polish public services (GUGiK). The application features a Python-based backend (FastAPI), a PostgreSQL database for relational data storage, and a modern React frontend for an intuitive user experience.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [API Overview](#api-overview)
- [Project Structure](#project-structure)
- [Additional Notes](#additional-notes)
- [Author](#author)

## Features

- Integration with GUGiK SOAP API for hierarchical address data retrieval
- Relational database schema using PostgreSQL
- FastAPI backend exposing a REST API for querying address data
- React-based frontend with live search and filter functionality
- Modular component architecture with Vite-based development workflow

## Requirements

### Backend (Python)

- Python 3.10 or higher
- PostgreSQL
- `zeep`, `psycopg2`, `requests`, `configparser`
- `fastapi`, `uvicorn`

### Frontend (React)

- Node.js
- npm

## Installation

### 1. Clone the repository

````bash
git clone https://github.com/your-user/address-browser.git
cd address-browser


### 2. Backend Setup

- Edit `Backend/.env` with your PostgreSQL credentials and the WSDL endpoint from GUGiK.

- Install backend dependencies:

```bash
pip install -r requirements.txt
````

- Import address data by running:

```bash
python Backend/data_importer.py
```

- Start the FastAPI server:

```bash
uvicorn Backend.search:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd address-search-app
npm install
npm run dev
```

This will launch the development server at [http://localhost:5173](http://localhost:5173), assuming the default Vite configuration.

## API Overview

Based on the source code of `search.py`, your FastAPI backend exposes multiple search endpoints for querying address data at different administrative levels. Here's a rewritten and professional **API Overview** section that accurately reflects the functionality of the project:

---

## API Overview

The backend exposes a set of RESTful endpoints via FastAPI for querying address components stored in the PostgreSQL database.

### Base URL

```
http://localhost:8000
```

### Endpoints

#### `GET /search/counties`

Search for counties (`powiaty`) matching a query string.

---

#### `GET /search/communes`

Search for communes (`gminy`) within a given county.

---

#### `GET /search/localities`

Search for localities (`miejscowości`).

---

#### `GET /search/streets`

Search for streets (`ulice`) based on a locality.

---

#### `GET /browse/voivodeship`

Returns a list of all voivodeships (`województwa`).

---

#### `GET /browse/county`

Returns all counties belonging to a specific voivodeship.

---

#### `GET /browse/commune`

Returns all communes within a specific county.

---

#### `GET /browse/locality`

Returns all localities within a given commune.

---

#### `GET /browse/street`

Returns all streets within a given locality.

---

#### `GET /browse/address`

Returns addresses based on a specific street.

---

## Project Structure

```
address-browser/
├── Backend/                            # Backend logic and database access
│   ├── sql/                            # SQL scripts and helper modules
│   │   ├── insert.py
│   │   ├── queries.py
│   │   ├── select_ID.py
│   │   ├── sequences.py
│   │   └── tables.py
│   ├── .env_example                    # Sample environment config file
│   ├── data_importer.py                # Script for downloading and importing address data from GUGiK
│   └── search.py                       # FastAPI app exposing the REST API
├── address-search-app/                # Frontend application built with React + Vite
│   ├── src/                            # Application source code
│   │   ├── archive/                    # (Possibly unused/legacy components)
│   │   │   ├── BrowseAddress.jsx       # Component for browsing hierarchical address data
│   │   │   ├── ResultsList.jsx         # Component for displaying search results
│   │   │   └── SearchBar.jsx           # Component for entering search queries
│   │   ├── App.jsx                     # Main React application component
│   │   ├── index.css                   # Global styles
│   │   └── main.jsx                    # Entry point for rendering the React app
│   ├── index.html                      # HTML template used by Vite
│   ├── package.json                    # Frontend dependencies and scripts
│   ├── postcss.config.js               # PostCSS configuration
│   ├── tailwind.config.js              # Tailwind CSS settings
│   └── vite.config.js                  # Vite development/build configuration
├── .gitignore                          # Git ignored files
├── README.md                           # Main project documentation
├── package-lock.json                   # npm lockfile for consistent installs
└── requirements.txt                    # Python backend dependencies


```

## Additional Notes

- The GUGiK API may occasionally be unavailable due to maintenance.
- Initial data import can take several hours due to the size and depth of the address browse.
- The importer includes basic error handling and retry logic for unstable connections.
- Ensure CORS is enabled in `search.py` if the frontend and backend are served from different origins.
- Unit tests are not included in this version.

## Author

Jan Weis  
GitHub: [https://github.com/Weisjan](https://github.com/Weisjan)

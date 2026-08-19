# KTRU Stacks

KTRU Stacks is a database-backed web application for exploring and locating music in KTRU Rice Radio's physical collection. It turns catalog metadata and shelf labels into practical browsing tools for station staff and listeners.

The application currently works with more than 30,000 album records and supports browsing by genre, style, artist, decade, and physical stack location.

## Highlights

- Browse the catalog by genre, style, artist, decade, or shelf location
- Search and filter album results in the browser
- View album artwork, metadata, track listings, and shelf labels
- Locate a physical album from its catalog or barcode identifier
- Visualize the station's CD and vinyl stacks and highlight the relevant shelf
- Register and sign in with securely hashed passwords
- Save favorite albums and create personal playlists
- Store catalog, account, favorite, and playlist data in SQLite

## Why I Built It

KTRU manages a large physical music collection whose usefulness depends on accurate catalog data and clear location information. KTRU Stacks connects that data to a web interface, making the collection easier to search, browse, verify, and navigate.

The project combines front-end development, database design, catalog management, and iterative troubleshooting around a real institutional workflow at Rice University.

## Technology

- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Database:** SQLite, SQLAlchemy ORM
- **Frontend:** HTML, CSS, JavaScript, Jinja templates
- **Authentication:** Werkzeug password hashing and Flask sessions
- **Deployment:** Gunicorn with a Procfile
- **Version control:** Git and GitHub

## Project Structure

```text
ktrustacks/
|-- app.py              # Flask routes, data models, and application logic
|-- lists.py            # Browsing categories and stack labels
|-- albums.db           # Development catalog database
|-- requirements.txt    # Python dependencies
|-- Procfile            # Gunicorn deployment command
|-- static/
|   `-- styles.css      # Application styling
`-- templates/          # Jinja page templates and browser-side behavior
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/matthewlbitz/ktrustacks.git
cd ktrustacks
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows, activate it with:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure a session secret

```bash
export SECRET_KEY="replace-this-with-a-long-random-value"
```

On Windows PowerShell:

```powershell
$env:SECRET_KEY="replace-this-with-a-long-random-value"
```

### 5. Start the application

```bash
python app.py
```

Then open [http://localhost:5000](http://localhost:5000).

## Data Model

The application uses relational models for:

- **Albums:** catalog metadata, artwork, track listings, and shelf locations
- **Songs:** tracks associated with albums
- **Users:** accounts with hashed passwords
- **Favorites:** a many-to-many relationship between users and albums
- **Playlists:** user-created collections connected to individual songs

## What This Project Demonstrates

- Building a content-rich web application with Flask and JavaScript
- Designing and querying a relational database with SQLAlchemy
- Translating physical collection workflows into practical digital tools
- Maintaining and verifying structured catalog data
- Troubleshooting UI, data, and application behavior
- Iterating on features through Git and GitHub collaboration

## Current Status

This is an actively developed operational project. Current work focuses on improving data quality, refining catalog workflows, strengthening application configuration, and making the interface more consistent and accessible.

## Author

**Matthew Bitz**<br>
Computer Science, Rice University<br>
[GitHub](https://github.com/matthewlbitz)

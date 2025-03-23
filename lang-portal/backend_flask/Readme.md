## Setting up the database

```sh
uv run -m invoke init-db
```

This will do the following:
- create the words.db (SQLite3 database)
- run the migrations found in `sql/setup/`
- load the seed data found in `seed/`

Please note that migrations and seed data is manually coded to be imported in the `lib/db.py`. So you need to modify this code if you want to import other seed data.

## Database Structure

The database contains Spanish vocabulary words organized into groups:
- Core Verbs: Common Spanish verbs with pronunciation guides
- Core Adjectives: Common Spanish adjectives with pronunciation guides

Each word entry includes:
- Spanish text
- Pronunciation guide with English phonetics
- English translation
- Word parts for learning components

## Clearing the database

Simply delete the `words.db` to clear entire database.

## Running the backend API

```sh
uv run app.py 
```

This should start the flask app on port `5000`

# Plan: Converting Japanese Learning App to Spanish Learning App

This document outlines the steps required to convert our Japanese language learning application to a Spanish language learning application. Each task is designed to be self-contained and can be implemented independently.

## 1. Database Schema Updates

- [x] **Task 1.1: Update database schema**
  - Modify `/backend_flask/sql/setup/create_table_words.sql` to rename columns from Japanese-specific to Spanish-specific names
  - `kanji` → `spanish`
  - `romaji` → `pronunciation`
  - Prompt: "Update the SQL table creation script in create_table_words.sql to rename columns from Japanese-specific to Spanish-specific names (kanji to spanish, romaji to pronunciation, keep other columns as is)"

- [x] **Task 1.2: Update database initialization code**
  - Modify `/backend_flask/lib/db.py` to use the new column names when importing word data
  - Update SQL queries to reference the new column names
  - Prompt: "Update the database initialization code in db.py to use the new column names (spanish instead of kanji and pronunciation instead of romaji) when inserting word data and in relevant queries"

## 2. Data Files Creation

- [x] **Task 2.1: Rename existing Japanese data files**
  - Rename `/backend_flask/seed/data_verbs.json` to `/backend_flask/seed/data_verbs_old.json`
  - Rename `/backend_flask/seed/data_adjectives.json` to `/backend_flask/seed/data_adjectives_old.json`
  - Prompt: "Rename the existing Japanese data files: data_verbs.json to data_verbs_old.json and data_adjectives.json to data_adjectives_old.json for backup purposes"

- [x] **Task 2.2: Create Spanish verbs JSON file**
  - Create `/backend_flask/seed/data_verbs.json` with common Spanish verbs
  - Follow the specified data structure with Spanish words
  - Include syllable breaks, capitalization for stress, and English approximation in pronunciation
  - Prompt: "Create a new JSON file called data_verbs.json with 60 common Spanish verbs following this structure: 
  ```json
  {
    "spanish": "hablar",
    "pronunciation": "ah-BLAR",
    "english": "to speak",
    "parts": [
      { "spanish": "habl", "pronunciation": "ah-bl" },
      { "spanish": "ar", "pronunciation": "AR" }
    ]
  }
  ```
  Include syllable breaks with hyphens, capitalization for stressed syllables, and English approximation of sounds in the pronunciation."

- [x] **Task 2.3: Create Spanish adjectives JSON file**
  - Create `/backend_flask/seed/data_adjectives.json` with common Spanish adjectives
  - Follow the specified data structure with Spanish words
  - Include syllable breaks, capitalization for stress, and English approximation in pronunciation
  - Prompt: "Create a new JSON file called data_adjectives.json with 60 common Spanish adjectives following this structure: 
  ```json
  {
    "spanish": "bueno",
    "pronunciation": "BWEH-no",
    "english": "good",
    "parts": [
      { "spanish": "bue", "pronunciation": "BWEH" },
      { "spanish": "no", "pronunciation": "no" }
    ]
  }
  ```
  Include syllable breaks with hyphens, capitalization for stressed syllables, and English approximation of sounds in the pronunciation."

## 3. Backend Code Updates

- [x] **Task 3.1: Update backend routes**
  - Modify API route handlers in the `/backend_flask/routes/` directory to use the new column names
  - Prompt: "Update the backend route handlers to reference 'spanish' instead of 'kanji' and 'pronunciation' instead of 'romaji' in all relevant files in the routes directory"

- [x] **Task 3.2: Update SQL queries**
  - Update all SQL queries in the codebase to use the new column names
  - Prompt: "Update all SQL queries throughout the codebase to use 'spanish' instead of 'kanji' and 'pronunciation' instead of 'romaji'"

## 4. Frontend Updates

- [x] **Task 4.1: Update API response handling**
  - Modify frontend code to handle the updated API response structure
  - Update references from `kanji` to `spanish` and `romaji` to `pronunciation`
  - Prompt: "Update the frontend API response handling code to reference 'spanish' instead of 'kanji' and 'pronunciation' instead of 'romaji'"

- [x] **Task 4.2: Update UI labels and text**
  - Change all UI references from Japanese to Spanish terminology
  - Update headers, labels, and instructional text
  - Prompt: "Update all UI labels, headers, and text to reference Spanish terminology instead of Japanese"

## 5. Testing

- [x] **Task 5.1: Update existing tests**
  - Update existing tests to use the new column names and Spanish test data
  - Prompt: "Update existing tests to use 'spanish' instead of 'kanji', 'pronunciation' instead of 'romaji', and Spanish test data"

- [x] **Task 5.2: Test database initialization**
  - Verify that the database initializes correctly with Spanish data
  - Prompt: "Create a test to verify that the database initializes correctly with Spanish data by running 'uv run -m invoke init-db' and checking that Spanish words are properly loaded"

## 6. Final Steps

- [x] **Task 6.1: Update documentation**
  - Update all documentation to reflect the Spanish learning focus
  - Prompt: "Update all documentation to reflect the Spanish learning focus instead of Japanese, ensuring all references to Japanese terminology are replaced with Spanish equivalents"

- [x] **Task 6.2: Initialize database with Spanish data**
  - Run the database initialization with the new Spanish data
  - Prompt: "Initialize the database with the new Spanish data using: uv run -m invoke init-db"

- [x] **Task 6.3: Verify application functionality**
  - Test the full application to ensure all functionality works with Spanish data
  - Prompt: "Test the complete application flow to ensure all functionality works with Spanish data by running the backend with 'uv run app.py' and testing all features through the frontend"

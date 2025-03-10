# Backend Technical Specs

## Business Goal
A language learning school wants to build a prototype of a Spanish language learning portal which will act as three things:
- Inventory of possible vocabulary that can be learned
- Act as a  Learning record store (LRS), providing correct and wrong score on practice vocabulary
- A unified launchpad to launch different learning apps

## Technical Requirements

- The backend will be built using Python 3.11 as the programming language
- Flask as the web framework
- SQLite3 as the database
- Git for version control
- GitHub for code hosting
- Pytest for testing
- The API will always return JSON
- There will be no authentication or authorisation
- Everything will be treated as a single user


## Database Schema

Our database will be a single sqlite3 database called `words.db` that will be in the root of the project folder of `backend_flask`.

We have the following tables:

words — Stores Spanish vocabulary words.
  - `id` (Integer, Primary Key): Unique identifier for each word
  - `spanish` (String, Required): The word written in Spanish
  - `english` (String, Required): English translation of the word
  - `parts` (JSON, Required): Word components stored in JSON format

groups — thematic groups of words.
  - `id` (Primary Key): Unique identifier for each group
  - `name` (String, Required): Name of the group
  - `words_count` (Integer, Default: 0): Counter cache for the number of words in the group

word_groups — join-table enabling many-to-many relationship between words and groups.
  - `id` (Primary Key): Unique identifier for each relationship
  - `word_id` (Foreign Key): References words.id
  - `group_id` (Foreign Key): References groups.id

study_activities — Defines different types of study activities available, linking a study session to group.
  - `id` (Primary Key): Unique identifier for each activity
  - `name` (String, Required): Name of the activity (e.g., "Flashcards", "Quiz")
  - `url` (String, Required): The full URL of the study activity

study_sessions — Records of study sessions grouping word_review_items.
  - `id` (Primary Key): Unique identifier for each session
  - `group_id` (Foreign Key): References groups.id
  - `study_activity_id` (Foreign Key): References study_activities.id
  - `created_at` (Timestamp, Default: Current Time): When the session was created

word_review_items — a record of word practice determining if the word was correct or not.
  - `id` (Primary Key): Unique identifier for each review
  - `word_id` (Foreign Key): References words.id
  - `study_session_id` (Foreign Key): References study_sessions.id
  - `correct` (Boolean, Required): Whether the answer was correct
  - `created_at` (Timestamp, Default: Current Time): When the review occurred


## API Endpoints

### GET /api/dashboard/last_study_session
- Returns the most recent study session

#### JSON Response:
```json
{
  "id": 123,
  "study_activity": {
    "id": 1,
    "name": "Flashcards"
  },
  "group": {
    "id": 2,
    "name": "Common Verbs"
  },
  "created_at": "2025-03-10T09:30:45Z",
  "stats": {
    "correct_count": 15,
    "wrong_count": 5,
  }
}
```

### GET /api/dashboard/study_progress
- returns the current study progress statistics.

#### JSON Response

```json
{
  "total_words_studied": 75,
  "total_words_available": 120,
  "mastery_percentage": 62.5,
  "total_study_time": "01:05:30"
}
```

### GET /api/dashboard/quick_stats
- returns the current study progress statistics.

#### JSON Response

```json
{
  "success_rate": 75.5,
  "total_study_sessions": 10,
  "total_active_groups": 4,
  "study_streak_days": 28
}
```

### GET /api/study_activities/:id
- returns the study activity with the given id

#### JSON Response:
```json
{
  "id": 1,
  "name": "Flashcards",
  "description": "Practice vocabulary with digital flashcards",
  "thumbnail_url": "https://example.com/images/flashcards.jpg"
}
```

### GET /api/study_activities/:id/study_sessions
- returns a list of study sessions associated with the study activity
- pagination with 100 items per page

#### JSON Response:
  ```json
  {
    "items": [
      {
        "id": 123,
        "activity_name": "Flashcards",
        "group_name": "Common Verbs",
        "start_time": "2025-03-10T09:30:45Z",
        "end_time": "2025-03-10T09:45:12Z",
        "review_items_count": 20
      },
      {
        "id": 124,
        "activity_name": "Vocabulary Quiz",
        "group_name": "Food Vocabulary",
        "start_time": "2025-03-09T14:20:30Z",
        "end_time": "2025-03-09T14:35:15Z",
        "review_items_count": 15
      }
    ],
    "pagination": {
      "total_items": 100,
      "total_pages": 1,
      "current_page": 1,
      "items_per_page": 100
    }
  }
  ```

### POST /api/study_activities/:id/launch

#### Request Params:
- group_id integer
- study_activity_id integer

#### JSON Response:
```json
{
  "study_session": {
    "id": 125,
    "group_id": 2,
    "study_activity_id": 1,
    "launch_url": "https://example.com/flashcards?session=125&group=2"
  }
}
```

### GET /api/words 
- pagination with 100 items per page.

#### JSON Response:
```json
{
  "items": {
      "id": 1,
      "spanish": "hablar",
      "english": "to speak",
      "correct_count": 12,
      "wrong_count": 3
    },
  "pagination": {
    "total_items": 120,
    "total_pages": 2,
    "current_page": 1,
    "items_per_page": 100
  }
}
```

### GET /api/words/:id
- Retrieves detailed information about a specific word

#### JSON Response:
```json
{
  "spanish": "hablar",
  "english": "to speak",
  "parts": {
    "stem": "habl",
    "ending": "ar",
    "type": "regular verb"
  },
  "stats": {
    "correct_count": 12,
    "wrong_count": 3,
  },
  "groups": [
    {
      "id": 2,
      "name": "Common Verbs"
    },
    {
      "id": 5,
      "name": "Basic Vocabulary"
    }
  ]
}
```

### GET /api/groups
- Paginated list of groups with 100 items per page.

#### JSON Response:

```json
{
  "items": {
      "id": 1,
      "name": "Basic Vocabulary",
      "words_count": 50
    },
  "pagination": {
    "total_items": 8,
    "total_pages": 1,
    "current_page": 1,
    "items_per_page": 100
  }
}
```

### GET /api/groups/:id
- Returns the name and group stats

#### JSON Response:
```json
{
  "id": 2,
  "name": "Common Verbs",
  "stats  ": {
    "words_count": 30
  }
}
```

### GET /api/groups/:id/words
- list all words in a group

#### JSON Response:
```json
{
  "items": {
      "id": 1,
      "spanish": "hablar",
      "english": "to speak",
      "correct_count": 12,
      "wrong_count": 3
  },
  "pagination": {
    "total_items": 300,
    "total_pages": 3,
    "current_page": 1,
    "items_per_page": 100
  }
}
```

### GET /api/groups/:id/study_sessions
- list of study sessions associated with the group

#### JSON Response:

```json
{
  "items": [
    {
      "id": 123,
      "activity_name": "Flashcards",
      "group_name": "Common Verbs",
      "start_time": "2025-03-10T09:30:45Z",
      "end_time": "2025-03-10T09:45:12Z",
      "review_items_count": 20
    }
  ],
  "pagination": {
    "total_items": 120,
    "total_pages": 2,
    "current_page": 1,
    "items_per_page": 100
  }
}
```

### GET /api/study_sessions
- Paginated list of sessions with 100 items per page.

#### JSON Response:
```json
{
  "items": {
      "id": 123,
      "activity_name": "Flashcards",
      "group_name": "Common Verbs",
      "start_time": "2025-03-10T09:30:45Z",
      "end_time": "2025-03-10T09:45:12Z",
      "review_items_count": 20
    },
  "pagination": {
    "total_items": 200,
    "total_pages": 2,
    "current_page": 1,
    "items_per_page": 100
  }
}
```

### GET /api/study_sessions/:id
- show a study session details

#### JSON Response:
```json
{
  "id": 123,
  "activity_name": "Flashcards",
  "group_name": "Common Verbs",
  "start_time": "2025-03-10T09:30:45Z",
  "end_time": "2025-03-10T09:45:12Z",
  "stats": {
    "correct_count": 15,
    "wrong_count": 5,
    "review_items_count": 20,
    "success_rate": 75.0
  }
}
```

### GET /api/study_sessions/:id/words 
- the list of review items in a specific study session

#### JSON Response:
```json
{
  "items": {
    "id": 1,
    "spanish": "hablar",
    "english": "to speak",
    "correct_count": 12,
    "wrong_count": 3
  },
  "pagination": {
    "total_items": 250,
    "total_pages": 3,
    "current_page": 1,
    "items_per_page": 100
  }
}
```

### POST /api/study_sessions
	- create a session

#### Request Params:
- group_id integer
- study_activity_id integer

#### JSON Response:
```json
{
  "study_session": {
    "id": 125,
    "group_id": 2,
    "study_activity_id": 1,
    "created_at": "2025-03-10T12:51:37Z"
  }
}
```

### POST /api/reset_history
- This will delete all study sessions and review items.

#### JSON Response:
```json
{
  "success": true,
  "message": "All study sessions and review items have been deleted",
}
```

### POST /api/full_reset
- This will drop all tables and re-create with seed data.

#### JSON Response:
```json
{
  "success": true,
  "message": "Database has been reset and seeded with initial data",
}
```

### POST /api/study_sessions/:id/words/:word_id/review
- Creates a new word review entry that records whether the user answered correctly or incorrectly during a specific study session

#### Required Params:
- correct boolean
- word_id integer
- id (study_session_id) integer

#### Request Payload:

```json
{
  "correct": true,
}
```

#### JSON Response:

```json
{
  "success": true,
  "word_id": 3,
  "study_session_id": 123,
  "correct": true,
  "created_at": "2025-03-10T12:51:37Z"
}
```

## Invoke Tasks

Invoke is a task runner for python.

Below is a list of tasks we need for our lang portal.

### Initialize Database
This task will initialize the sqlite database called `words.db`.

### Migrate Database
This task will run a series of migrations of sql files on the database.

Migrations live in the `migrations` folder.
The migration files will run in order of their filename.
The file names should look like this: 

```sql
0001_init.sql
0002_create_words_table.sql
0003_create_groups_table.sql
```

### Seed Data
This task will import json files and transform them into database records.

All seed files live in the `seeds` folder.
In our task we should have DSL to each specific seed file and it's expected group word name.

```json
[
  {
    "spanish": "hablar",
    "english": "to speak",
    "parts": {
      "stem": "habl",
      "ending": "ar",
      "type": "regular verb"
    }
  }
]
```
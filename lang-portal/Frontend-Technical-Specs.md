## Frontend Technical Specs

## Pages

### Dashboard `/dashboard`

#### Purpose
The purpose of this page is to provide a summary of the user's learning journey and act as the default page when a user visits the web-app.

#### Components
- Last Study Session
  - shows last activity used
  - shows when last activity was used
  - summarizes wrong vs correct from last activity
  - has a link to the group

- Study Progress
  - total words study eg. 5/120
    - across all study sessions show the total words studied out of all possible words in our database.
  - display a mastery progress eg. 50%
  - display total study time eg. 5:30

- Quick Stats
  - success rate eg. 75%
  - total study sessions eg. 10
  - total active groups eg. 4
  - study streak eg. 28 days

- Start Studying Button
  - goes to study activities page

#### Required API Endpoints

- GET /api/dashboard/last_study_session => returns the most recent study session
- GET /api/dashboard/study_progress => returns the current study progress
- GET /api/dashboard/quick_stats => returns the quick stats

### Study Activities Index`/study_activities`

#### Purpose
The purpose of this page is to show a collection of study activities available to the user with a thumbnail and it's name, with an option(buttons) to either view or launch a study activity.

#### Components

- Study Activity Card
  - show a thumbnail of the study activity
  - the name of the study activity
  - a launch button to take the user to the launch page
  - a "view" button to take the user to the study activity page to access more information about the activity, including past study sessions related to it.

#### Required API Endpoints

- GET /api/study_activities => returns a list of all study activities

### Study Activity Show `/study_activities/:id`

#### Purpose
The purpose of this page is to show the details of a study activity and the past study sessions related to it.

#### Components
- Name of the study activity
- Thumbnail of the study activity
- Description of the study activity
- Button to launch the study activity
- Paginated list of past study sessions
  - id
  - activity name
  - group name
  - start time
  - end time (inferred by the last word_review_item submitted)
  - number of review items

#### Required API Endpoints
- GET /api/study_activities/:id => returns the study activity with the given id
- GET /api/study_activities/:id/study_sessions => returns a list of study sessions associated with the study activity

### Study Activites Launch `/study_activities/:id/launch`

#### Purpose
The purpose of this page is to launch a study activity.

#### Components
- Name of the study activity
- Launch form
  - select field for group
  - launch now button

#### Behaviour
After the form is submitted:
- a new tab opens with the study activity based on the associated URL provided in the database.
- the page will redirect to the study session show page.

#### Required API Endpoints
- POST /api/study_activities/:id/launch
- POST /api/study_sessions

### Words Index `/words`

#### Purpose
The purpose of this page is to show all spanish words in our database.

#### Components
- Paginated word list
  - Columns
    - Spanish
    - English
    - Correct count
    - Wrong count
  - Pagination with 100 items per page
  - Clicking the spanish word will take us to the word show page

#### Required API Endpoints
- GET /api/words

### Word Show `/words/:id`

#### Purpose
The purpose of this page to show information about a specific word.

#### Components
- Spanish
- English
- Study Statistics
  - Correct count
  - Wrong count
- Word Groups
  - show a series of pills eg. tags
  - when group name is clicked it will take us to the group show page

#### Required API Endpoints
- GET /api/words/:id => returns the word with the given id

### Word Groups Index `/groups`

#### Purpose
The purpose of this page is to show a list of groups in our database.

#### Components
- Paginated group list
  - Columns
    - Group name
    - Word count
  - Clicking the group name will take us to the group show page

#### Required API Endpoints
- GET /api/groups

### Group Show `/groups/:id`

#### Purpose
The purpose of this page is to show information about a specific group.

#### Components
- Group name
- Group Statistics
  - Total Word count
- Words in Group (Paginated list of words)
  - Should use the same component as the student sessions
- Study Sessions (Paginated list of study sessions)
  - Should use the same component as the student sessions index page

#### Required API Endpoints
- GET /api/groups/:id (the name and group stats)
- GET /api/groups/:id/words (the list of words in the group)
- GET /api/groups/:id/study_sessions (the list of study sessions associated with the group)

### Study Sessions Index `/study_sessions`

#### Purpose
The purpose of this page is to show a list of study sessions associated with the current user.

#### Components
- Paginated study session list
  - Columns
    - Id
    - Activity name
    - Group Name
    - Start time
    - End time
    - Number of review items
  - Clicking the study session id will take us to the study session show page

#### Required API Endpoints
- GET /api/study_sessions

### Study Session Show `/study_sessions/:id`

#### Purpose
The purpose of the page is to show information about a specific study session.

#### Components
- Study session details:
  - Activity name
  - Group Name
  - Start time
  - End time
  - Number of review items
- Words review items (paginated list)
  - Should use the same component as the word index page

#### Required API Endpoints
- GET /api/study_sessions/:id (the study session details)
- GET /api/study_sessions/:id/words (the list of review items in the study session)

### Settings Page

#### Purpose
The purpose of this page is to make configurations to the learning portal.

#### Components
- Theme selection eg. Light, Dark, System Default
- Reset history button
  - This will delete all study sessions and review items
- Full Reset button
  - This will drop all tables and re-create with seed data

#### Required API Endpoints
- POST /api/reset_history
- POST /api/full_reset

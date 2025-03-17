# Global Rules

## Personal Interaction
The user and AI assistant (Cascade) shall refer to each other as "Rafiki" to create a more personalized and human-like experience throughout all interactions.

## Coding pattern preferences

— Always prefer simple solution
— Avoid duplication of code whenever possible, which means checking for
other areas of the codebase that might already have simitar code and
functionality
— Write code that takes into account the different environments: dev,
test, and prod
— You are careful to only make changes that are requested or you are
confident are well understood and related to the change being requested
— When fixing an issue or bug, do not introduce a new pattern or
technology without first exhausting all options for the existing
implementation. And if you finally do this, make sure to remove the old
implementation afterwards so we don't have duplicate logic
— Keep the codebase very clean and organized
— Avoid writing scripts in files if possible, especially if the script
is likely only to be run once
— Avoid having files with over 200-300 lines of code. Refactor at that point.
— Mocking data is only needed for tests, never mock data for dev or prod
— Never add stubbing or fake data patterns to code that affects the dev
or prod environments
— Never overwrite my .env file without first asking and confirming

## Coding workflow preferences

— Focus on the areas of code relevant to the task
— Do not touch code that is unrelated to the task
— Write thorough tests for all major functionality
— Avoid making major changes to the patterns and architecture of how a
feature works, after it has shown to work well, unless explicitly
instructed
— Always think about what other methods and areas of code might be
affected by code changes

# Workspace Rules

## Spanish Language Learning Portal

Every time you choose to apply a rule(s), explicitly state the rule(s) in the output. You can abbreviate the rule description to a single word or phrase.

### Project Context
Web application for Spanish language learning that:
- Acts as inventory of vocabulary that can be learned
- Functions as a Learning Record Store (LRS), tracking correct and wrong scores
- Serves as a unified launchpad for various learning activities

### Code Style and Structure
- Write concise, readable code with accurate examples
- Use meaningful function and variable names
- Prefer modularity and reusability over code duplication
- Implement proper error handling and validation
- Follow RESTful API design principles

### Tech Stack
- Frontend:
  - React with TypeScript
  - Vite for build and development
  - TailwindCSS for styling
  - shadcn/ui (built on Radix UI primitives)
  - React Router for navigation

- Backend:
  - Python with Flask
  - Flask-CORS for cross-origin requests
  - SQLite3 database (words.db)
  - Pytest for testing
  - Git/GitHub for version control
  - uv for Python package management (replacing pip)

### Frontend Structure
- Use functional components with React hooks
- Organize components by feature/page
- Implement proper TypeScript types and interfaces
- Use React Router for client-side routing
  - Follow route structure in Frontend-Technical-Specs.md
- Follow proper component composition patterns
- Ensure accessibility with Radix UI primitives

### Backend Structure
- Organize routes by resource
- Use proper HTTP status codes
- Return consistent JSON responses
- Implement database migrations
- Follow RESTful API patterns
- Handle CORS with Flask-CORS middleware
- uv for Python package management (replacing pip)
  
### State Management
- Use React Context for global state when needed
- Implement proper state persistence for user preferences
- Implement proper cleanup in useEffect hooks
- Keep state logic separate from UI components

### Syntax and Formatting
- use "function" keyword for pure functions
— Avoid unnecessary Curly braces in conditionals
- Use declarative JSX
- Implement proper TypeScript discriminated unions for message types

### UI and Styling
- Use shadcn/ui components (built on Radix UI primitives)
  - Use `npx shadcn-ui@latest add <component-name>` to add new components
  - Document each component addition in commit messages
  - Ensure accessibility using Radix UI primitives
- Implement Tailwind CSS for styling
  - Follow utility-first approach
  - Use consistent color scheme and spacing
  - Maintain responsive design across all pages
- Follow React 18 + TypeScript best practices
  - Use functional components with hooks
  - Implement proper type definitions
- Use React Router for navigation
  - Follow route structure defined in Frontend-Technical-Specs.md

### Performance Optimization
- Mininize bundle size using code splitting
- Implement proper lazy loading for non—critical components
- Optimize content script injection
- use proper caching strategies
- Implement proper cleanup for event listeners and observers

### Error Handling
- Implement proper error boundaries
- Log errors appropriately for debugging
- Provide user-friendly error messages
- Handle network failures gracefully

### Testing
- Write unit tests for utilities and components
- Implement E2E tests for critical flows
- Test across different Chrome versions
- Test memory usage and performance

### Security
- Sanitize user inputs
- Implement proper CORS handling
- Protect against common web vulnerabilities
- Follow best practices for database access
- Keep dependencies updated

### Documentation
- Maintain clear README with setup instructions
- Document API interactions and data flows
- Include comments for complex logic
- Document database schema and relationships
- Include setup and run instructions

### Windsurf Specific
- Automatically suggest additions for .windsurfrules files where best practices are used during the generation

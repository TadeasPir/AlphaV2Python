
# Game library databse manager by Tadeas Pirich

This project is a **game library management system** that facilitates the management of users, games, achievements, reviews, libraries, and reports. It provides functionalities for importing data, managing database records, and generating reports.

## Table of Contents

-   [Overview](#overview)
-   [Features](#features)
-   [Project Structure](#project-structure)
-   [Installation](#installation)
-   [Usage](#usage)
-   [Dependencies](#dependencies)
-   [Contributing](#contributing)

## Overview

The system allows users to:

-   Import users and games from external sources.
-   Manage user, game, achievement, and review records.
-   Store and update user game libraries.
-   Generate and save reports.

It is built with Python and uses a MySQL database for data storage.

## Features

-   **User Management**: Add, update, delete, and retrieve user records.
-   **Game Management**: Manage game details, including genre, price, and multiplayer capabilities.
-   **Library Management**: Track user purchases and game ownership.
-   **Achievement Management**: Add and manage achievements earned by users.
-   **Review System**: Manage user reviews for games.
-   **Data Import**: Import users and games from CSV and JSON files.
-   **Reporting**: Generate and save structured reports from database views.

## Project Structure

-   `genre_enum.py`: Defines the `GenreEnum` class for managing game genres.
-   `importing.py`: Functions for importing user and game data from CSV and JSON files.
-   `library.py`: Manages the user-game relationships in the library database.
-   `report.py`: Handles the generation and saving of system reports.
-   `review.py`: Manages user reviews for games.
-   `user.py`: Handles user-related operations like creation, deletion, and updates.
-   `achievement.py`: Manages user achievements.
-   `game.py`: Handles game-related operations, including validation against the `GenreEnum`.

## Installation

1.  Clone the repository:
    
    bash
    
    ZkopírovatUpravit
    
    `git clone <https://github.com/TadeasPir/AlphaV2Python>
   cd <AlphaV2Python>` 
    
2.  Install dependencies:
    
    bash  run
    
    `pip install -r requirements.txt` 
    
3.  Set up the database:
    
    -   Configure the database connection in the `config.yaml`.
    -   Run the necessary SQL migrations.
    
4.  Set up virtual environments for better dependency management.
5. 
    ### Configuration Format (config.yaml)
```yaml
db:  
  host: "localhost"  
  user: "root"  
  password: ""  
  database: "GameLibraryDB"  
  
logging:  
  level: "ERROR"  
  file: "app.log"
```
logging has these levels (DEBUG, INFO, WARNING, ERROR)
## Project struture 
```plaintext
src/
├── config.yaml                     # Configuration file for database and logging settings
├── models/
│   ├── achievement.py              # Manages user achievements
│   ├── game.py                     # Handles game-related operations
│   ├── genre_enum.py               # Defines game genres as an enumeration
│   ├── importing.py                # Functions for importing users and games
│   ├── library.py                  # Manages user-game relationships
│   ├── report.py                   # Generates and saves reports
│   ├── review.py                   # Manages user reviews
│   └── user.py                     # Manages user records
├── ui/
│   ├── achievement_console.py      # Console interface for achievements
│   ├── game_console.py             # Console interface for games
│   ├── library_console.py          # Console interface for libraries
│   ├── reports_console.py          # Console interface for reports
│   ├── review_console.py           # Console interface for reviews
│   └── user_console.py             # Console interface for users
├── database/
│   └── databse.py                  # database connector
├── app_console.py                  # Main console application
└── utils.py                        # Utility functions (e.g., logging setup)
```
    

## Usage



### Library Management

-   Add a game to a user's library:
    
    python
    
    ZkopírovatUpravit
    
    `from library import Library
    library = Library(user_id=1, game_id=1, purchase_date='2023-01-01', has_dlc=False)
    library.save()` 
    

### Reporting

-   Generate a game overview report:
    
    python
    
    

    
---

## Sources

- [SPŠE Jecná Moodle](https://moodle.spsejecna.cz/mod/page/view.php?id=1940)
- [ChatGPT](https://chatgpt.com/)
- [Claude AI](https://claude.ai/)
### consulted
- Martin Hornych 
- Tomáš Križko 
- Ondra Kábrt
- Adam Hlaváčik

---
## Dependencies

-   Python 3.10 or above
-   MySQL Connector
-   Logging
-   CSV and JSON modules

## Contributing

Contributions are welcome! Please create an issue or submit a pull request for any bugs or feature requests.


## DB diagram

![image](https://github.com/user-attachments/assets/0ea0e513-2318-4797-bc5c-30448621c6bf)

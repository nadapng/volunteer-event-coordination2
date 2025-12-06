# Volunteer Event Coordination System

A comprehensive Python application for managing volunteers and events with a console-based user interface. This system allows organizations to efficiently manage volunteer registration, event coordination, and user administration.

## Features

- **User Management**: Create, update, delete, and list volunteers, organizers, and administrators
- **Event Management**: Organize events with capacity limits, location details, and scheduling
- **Registration System**: Register volunteers for events with status tracking (registered, waitlist, cancelled)
- **Role-based Access**: Support for different user roles (admin, organizer, volunteer)
- **Database Integration**: MySQL database backend for persistent data storage
- **Console Interface**: Interactive command-line interface for easy operation

## System Architecture

This application follows a layered architecture pattern:

```
├── Presentation Layer   (console_ui.py, user_interface.py)
├── Service Layer       (app_services.py)
├── Infrastructure Layer (user.py, event.py)
└── Persistence Layer   (mysql_persistence_wrapper.py)
```

## Prerequisites

- Python 3.13 or higher
- MySQL Server
- Git
- pipenv (for dependency management)

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd volunteer-event-coordination2
   ```

2. **Install dependencies**:

   ```bash
   pipenv install
   ```

3. **Set up the database**:

   ```bash
   # Navigate to database directory
   cd database

   # Make the initialization script executable
   chmod +x initialize_database.sh

   # Run the database setup
   ./initialize_database.sh
   ```

4. **Configure the application**:
   Edit `config/volunteer_event_coordination_app_config.json` to match your database settings:
   ```json
   {
     "database": {
       "connection": {
         "config": {
           "database": "volunteer_event_coordination",
           "user": "your_db_user",
           "password": "your_db_password",
           "host": "localhost",
           "port": 3306
         }
       }
     }
   }
   ```

## Usage

### Running the Application

```bash
# Using pipenv
pipenv run python src/main.py -c config/volunteer_event_coordination_app_config.json

# Or activate the virtual environment first
pipenv shell
python src/main.py -c config/volunteer_event_coordination_app_config.json
```

### Build Script

The project includes a build script for automated setup:

```bash
# Make the build script executable
chmod +x build.sh

# Run the build script
./build.sh
```

### Available Operations

Once the application starts, you can perform the following operations:

#### User Management

- **List all users**: View all registered users in the system
- **Add User**: Register new volunteers, organizers, or administrators
- **Update User**: Modify existing user information
- **Delete User**: Remove users from the system

#### Event Management

- **List all events**: View all scheduled events
- **Add Event**: Create new volunteer events with details like title, description, location, capacity, and schedule
- **Update Event**: Modify existing event information
- **Delete Event**: Remove events from the system

#### Registration Management

- **Register User to Event**: Sign up volunteers for specific events
- **Update Registration Status**: Change registration status (registered, waitlist, cancelled)
- **Unregister User**: Remove volunteers from events

## Database Schema

### Users Table

- `id`: Primary key (auto-increment)
- `full_name`: User's full name (VARCHAR 120)
- `email`: Unique email address (VARCHAR 160)
- `phone`: Contact number (VARCHAR 30)
- `role`: User role (admin, organizer, volunteer)
- `created_at`: Registration timestamp

### Events Table

- `id`: Primary key (auto-increment)
- `title`: Event title (VARCHAR 150)
- `description`: Event details (TEXT)
- `location`: Event venue (VARCHAR 150)
- `starts_at`: Event start time (DATETIME)
- `ends_at`: Event end time (DATETIME)
- `capacity`: Maximum volunteers (INT)
- `created_by`: Event creator (Foreign Key to users)
- `created_at`: Creation timestamp

### Volunteer Shift Cross-Reference Table

- `id`: Primary key (auto-increment)
- `event_id`: Foreign key to events
- `user_id`: Foreign key to users
- `status`: Registration status (registered, waitlist, cancelled)
- `registered_at`: Registration timestamp

## Development

### Project Structure

```
volunteer-event-coordination2/
├── config/                     # Configuration files
├── database/                   # Database scripts and migrations
│   ├── db_version_1/          # Database schema v1
│   └── logs/                  # Database operation logs
├── docs/                      # Documentation
├── logs/                      # Application logs
├── src/                       # Source code
│   ├── main.py               # Application entry point
│   └── volunteer_event_coordination/
│       ├── application_base.py
│       ├── logging.py
│       ├── settings.py
│       ├── infrastructure_layer/
│       ├── persistence_layer/
│       ├── presentation_layer/
│       └── service_layer/
└── tests/                     # Test suite
```

### Running Tests

```bash
# Run all tests
pipenv run pytest

# Run tests with coverage
pipenv run pytest --cov=src

# Run tests verbosely
pipenv run pytest -sv
```

### Dependencies

#### Production Dependencies

- `mysql-connector-python`: MySQL database connectivity
- `prettytable`: Console table formatting

#### Development Dependencies

- `pytest`: Testing framework
- `pytest-cov`: Test coverage reporting

## Configuration

The application uses JSON configuration files located in the `config/` directory. The main configuration includes:

- **Application metadata**: Version, name, logging prefix
- **Database settings**: Connection pool configuration, credentials
- **Logging configuration**: Log file settings and output formatting

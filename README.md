<img width="1902" height="919" alt="image" src="https://github.com/user-attachments/assets/e045c19f-730b-4d82-a824-8cb0141e4b02" />

# Bracket Creator

A web application for creating and managing single-elimination tournament brackets. This project was developed to provide a clean, ad-free alternative to existing bracket websites that are often cluttered with advertisements and unnecessary features.

## Overview

Bracket Creator allows users to create tournament brackets with customizable sizes and manage matches through each round until a champion is determined. The application features user authentication, bracket persistence, and an intuitive interface for tournament progression.

## Features

- User registration and authentication system
- Create brackets with various participant sizes (4, 8, 16, 32 players)
- Add and manage tournament participants
- Visual bracket display showing tournament progression
- Click-to-advance winner selection system
- Responsive design for desktop and mobile devices
- Clean, modern interface without advertisements
- Tournament state persistence across sessions

## Technology Stack

- **Backend**: Python 3.11, Django 5.2.2
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Django's built-in authentication system
- **Deployment**: Heroku with WhiteNoise for static file serving

## Installation and Setup

### Prerequisites
- Python 3.11 or higher
- PostgreSQL
- pip (Python package manager)

### Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd bracket-creator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/bracketcreatordb
```

5. Set up the database:
```bash
createdb bracketcreatordb
python manage.py migrate
```

6. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Usage

1. **Registration**: Create an account to start managing tournaments
2. **Create Bracket**: Choose a tournament name and select the number of participants
3. **Add Participants**: Enter names for all tournament participants
4. **Start Tournament**: Initialize the bracket to begin the first round
5. **Advance Winners**: Click the checkmark button next to winners to advance them to the next round
6. **Tournament Completion**: Continue until a champion is determined

## Project Structure

```
bracketcreator/
├── bracket_creator/          # Main Django application
│   ├── models.py            # Database models (TournamentBracket, Participant, Match)
│   ├── views.py             # Application views and business logic
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JavaScript, and static assets
├── bracketcreator/          # Django project settings
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## Database Schema

- **TournamentBracket**: Stores tournament metadata (name, size, creator, status)
- **Participant**: Individual tournament contestants linked to brackets
- **Match**: Represents individual matches with players, winners, and round information

## Deployment

The application is deployed on Heroku with the following configuration:
- PostgreSQL database addon
- WhiteNoise for static file serving
- Environment-based configuration for production settings

Live deployment: https://bracket-creator-app-fb67a7af1980.herokuapp.com/

## Future Enhancements

- Double-elimination bracket support
- Tournament statistics and analytics
- Bracket sharing and public viewing options
- Advanced tournament seeding options

## License

This project uses Django, which is licensed under the BSD License. See Django's official documentation for complete license details.

## Attributions

- Built with Django web framework

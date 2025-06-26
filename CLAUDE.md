# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a dual-implementation password generator project with both a Streamlit web application (Python) and a static HTML/JavaScript version for GitHub Pages deployment. The project focuses on security, Japanese language support, and user experience.

## Key Implementation Details

### Dual Architecture
- **Streamlit Version** (`app.py`): Full-featured with database support, batch generation up to 1000 passwords, and user preferences
- **Static Version** (`index.html`): Client-side only implementation for GitHub Pages, no server dependencies

### Core Components
- `password_generator.py`: Core generation logic with character set management including Japanese characters (hiragana, katakana, kanji)
- `strength_checker.py`: Entropy calculation and strength evaluation
- `utils.py`: Presets, export functions (TXT/CSV), security recommendations
- `database.py`: SQLAlchemy models for password history and user preferences (Streamlit version only)

## Development Commands

### Running the Streamlit Application
```bash
# Install dependencies (create requirements.txt first)
pip install streamlit sqlalchemy psycopg2-binary

# Run the application
streamlit run app.py
```

### Testing the Static Version
```bash
# Python 3
python -m http.server 8000

# Node.js
npx serve .
```

### Database Setup (if using Streamlit version)
- Requires PostgreSQL database
- Connection string format: `postgresql://user:password@host:port/dbname`
- Tables are auto-created on first run

## Important Architectural Decisions

### Character Sets
The application supports extensive character sets:
- Basic: numbers, lowercase, uppercase
- Symbols: organized into categories (basic, brackets, punctuation, math)
- Japanese: hiragana, katakana, common kanji
- Custom characters can be added

### Security Considerations
- Uses `secrets` module for cryptographically secure random generation
- Client-side generation in static version (no data sent to server)
- Password strength based on entropy calculation
- Avoids common patterns detection

### UI/UX Principles
- Batch generation displays all passwords in a single textarea
- One-click copy for all passwords
- No individual password strength indicators (simplified UI)
- Responsive design for mobile/desktop
- Default: 50 passwords, 16 characters

## Missing Dependencies File
Note: No `requirements.txt` exists. When creating one, include:
- streamlit
- sqlalchemy
- psycopg2-binary

## GitHub Pages Deployment
The `index.html` file is self-contained and ready for GitHub Pages deployment. Enable Pages in repository settings pointing to the main branch root.
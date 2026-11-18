# Sticky Notes Application (Django) \- Part 1

This project implements a Django sticky notes application with CRUD operations.

---

## Project Structure

```
06-049-1 Django – Sticky Notes Application Part 1/
├── 06-049-1 Django – Sticky Notes Application Part 1.pdf
└── source/
    ├── 01_use_case_diagram.mmd     # Part 1: Mermaid.js Use Case Diagram
    ├── 02_sequence_diagram.mmd     # Part 1: Mermaid.js Sequence Diagram (MVT flow)
    ├── 03_class_diagram.mmd        # Part 1: Mermaid.js Class Diagram
    ├── research_answers.md         # Part 2: Research questions on HTTP state & MariaDB
    ├── requirements.txt            # Single unified Python dependencies file
    ├── README.md                   # Project overview & running instructions
    ├── venv/                       # Project Python virtual environment (Homebrew Python 3.14)
    └── sticky_notes/               # Django Project root
        ├── manage.py               # Django CLI management script
        ├── db.sqlite3              # Initialized SQLite database with migrations & sample notes
        ├── static/                 # Collected static files
        ├── sticky_notes/           # Project configuration app
        │   ├── __init__.py
        │   ├── settings.py         # Configured with notes in INSTALLED_APPS & static settings
        │   ├── urls.py             # Root URL routing including notes.urls
        │   ├── asgi.py
        │   └── wsgi.py
        └── notes/                  # Sticky Notes application
            ├── __init__.py
            ├── admin.py            # Model registered with Django admin
            ├── apps.py
            ├── forms.py            # NoteForm ModelForm (title, content)
            ├── models.py           # Note model (title, content, created_at)
            ├── tests.py            # Unit tests covering CRUD views & model
            ├── urls.py             # URL patterns for CRUD operations
            ├── views.py            # Function-based CRUD views
            ├── migrations/
            │   ├── __init__.py
            │   └── 0001_initial.py # Initial migration creating the Note table
            ├── static/
            │   └── notes/
            │       └── styles.css  # Sticky note styling (yellow cards, pins, responsive)
            └── templates/
                ├── base.html       # Base layout template extended by other views
                └── notes/
                    ├── note_list.html   # Displays all notes with CRUD action links
                    ├── note_detail.html # Displays single note details & action buttons
                    └── note_form.html   # Create and Edit note form
```

---

## How to Run the Application

### 1\. Environment Setup Instructions

macOS / Linux:

```sh
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

&nbsp;

Windows

```sh
python3 -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt
```

### 2\. Run Database Migrations

Run database migrations to initialize tables:

```sh
cd sticky_notes
python manage.py migrate
```

### 3\. Run the Development Server

Start the local server:

```sh
python manage.py runserver
```

Visit [`http://127.0.0.1:8000/`](http://127.0.0.1:8000/) in your browser to view and use the Sticky Notes app\!

### 4\. Admin Access

An admin superuser is already initialized:

- **URL**: [`http://127.0.0.1:8000/admin/`](http://127.0.0.1:8000/admin/)  
- **Username**: `admin`  
- **Password**: `admin1234`

### 5\. Running the Automated Tests

From `source/sticky_notes` (the directory entered in step 2), run the unit test suite:

```sh
python manage.py test
```

All 7 unit tests will execute and confirm CRUD operations, form submissions, and routing integrity.

Run `deactivate` when finished.
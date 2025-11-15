# Project Structure

```
FaveNBAHoopers/
│
├── 📄 Core Application Files
│   ├── nba_stats_etl.py          # Main ETL pipeline (refactored from fave_nba_hoopers.py)
│   ├── config.py                 # Centralized configuration management
│   ├── analyze_stats.py          # Data analysis utilities and helper functions
│   └── setup.py                  # Interactive setup wizard for easy onboarding
│
├── 📋 Configuration Files
│   ├── requirements.txt          # Python dependencies with pinned versions
│   ├── .env.example             # Environment variables template (DO NOT COMMIT .env)
│   └── .gitignore               # Git ignore rules for Python projects
│
├── 📚 Documentation
│   ├── README.md                # Comprehensive project documentation
│   ├── QUICKSTART.md            # 5-minute getting started guide
│   ├── CHANGELOG.md             # Version history and migration guide
│   ├── REFACTORING_SUMMARY.md   # Technical details of the refactoring
│   └── PROJECT_STRUCTURE.md     # This file!
│
├── 💾 Data & Queries
│   ├── example_queries.sql      # 15+ ready-to-use SQL queries
│   ├── data/                    # Created automatically (local data storage)
│   └── logs/                    # Created automatically (application logs)
│
└── 📜 Legal
    └── LICENSE                   # MIT License
```

## File Purposes

### Core Application Files

#### `nba_stats_etl.py` (Main Application)
- **Purpose**: Main ETL pipeline that orchestrates data extraction, transformation, and loading
- **Key Features**:
  - Class-based design (`NBAStatsETL`)
  - Comprehensive error handling
  - Professional logging
  - Modular extract/transform/load methods
- **Usage**: `python nba_stats_etl.py`

#### `config.py` (Configuration Hub)
- **Purpose**: Centralized configuration management
- **Contains**:
  - Database connection settings
  - Player ID mappings
  - NBA divisions and conferences
  - Project path definitions
- **Benefits**: Single source of truth for all configuration

#### `analyze_stats.py` (Analysis Tools)
- **Purpose**: Quick data analysis without writing SQL
- **Features**:
  - `NBAStatsAnalyzer` class with helper methods
  - Career averages calculation
  - Recent form analysis
  - Player comparisons
  - Home vs away splits
- **Usage**: `python analyze_stats.py`

#### `setup.py` (Setup Wizard)
- **Purpose**: Guide users through initial setup
- **Features**:
  - Python version check
  - Dependency installation
  - .env file creation
  - Database connection test
  - Directory creation
- **Usage**: `python setup.py`

### Configuration Files

#### `requirements.txt`
```
nba-api==1.5.2          # NBA statistics API
pandas==2.2.0           # Data manipulation
numpy==1.26.3           # Numerical computing
sqlalchemy==2.0.25      # Database ORM
psycopg2-binary==2.9.9  # PostgreSQL adapter
python-dotenv==1.0.0    # Environment variables
```

#### `.env.example`
Template for environment variables. Copy to `.env` and fill in your credentials:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password_here
```

#### `.gitignore`
Prevents sensitive and unnecessary files from being committed:
- Python artifacts (`__pycache__`, `*.pyc`)
- Virtual environments (`venv/`, `env/`)
- Environment files (`.env`)
- Database files (`*.db`)
- IDE settings (`.vscode/`, `.idea/`)

### Documentation Files

#### `README.md` (Main Documentation)
Comprehensive guide covering:
- Project overview and features
- Tech stack
- Installation instructions
- Usage examples
- Data schema
- Configuration guide
- Troubleshooting
- Future enhancements

#### `QUICKSTART.md` (Getting Started)
Fast-track guide for new users:
- 5-minute setup process
- Quick analysis examples
- Common tasks
- Troubleshooting shortcuts

#### `CHANGELOG.md` (Version History)
Documents all changes:
- Version 2.0.0: Major refactor
- Version 1.0.0: Original release
- Migration guide from v1 to v2

#### `REFACTORING_SUMMARY.md` (Technical Details)
In-depth technical documentation:
- Detailed comparison of old vs new code
- Security improvements
- Code quality metrics
- Breaking changes
- Migration benefits

### Data & Queries

#### `example_queries.sql`
15+ production-ready SQL queries:
1. Career averages
2. Best performances
3. Home vs away comparison
4. Performance by day of week
5. Conference analysis
6. Recent form
7. Triple-doubles
8. 30+ point games
9. Monthly performance
10. Efficient scoring games
11. Year-over-year progression
12. Head-to-head matchups
13. Clutch performance
14. Career milestones
15. Consistency analysis

## Database Tables Created

After running the ETL pipeline:

```
PostgreSQL Database
├── lebron_james              # LeBron's complete career stats
├── stephen_curry             # Curry's complete career stats
├── damian_lillard            # Dame's complete career stats
├── trae_young                # Trae's complete career stats
├── giannis_antetokounmpo    # Giannis's complete career stats
└── nba_5                     # Combined comparison table (equal games per player)
```

## Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                        USER WORKFLOW                         │
└─────────────────────────────────────────────────────────────┘

1. Initial Setup
   └── python setup.py
       ├── Checks Python version
       ├── Installs dependencies
       ├── Creates .env file
       ├── Tests database connection
       └── Creates directories

2. Run ETL Pipeline
   └── python nba_stats_etl.py
       ├── EXTRACT: Fetch data from NBA API
       ├── TRANSFORM: Clean and enrich data
       └── LOAD: Write to PostgreSQL

3. Analyze Data
   ├── Option A: python analyze_stats.py
   │   └── Quick Python-based analysis
   │
   └── Option B: Use SQL queries
       └── Connect to PostgreSQL and run example_queries.sql

4. Customize (Optional)
   ├── Edit config.py to add/remove players
   ├── Modify transformation logic in nba_stats_etl.py
   └── Create custom analysis functions in analyze_stats.py
```

## Development Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT WORKFLOW                      │
└─────────────────────────────────────────────────────────────┘

1. Clone Repository
   └── git clone <repo-url> && cd FaveNBAHoopers

2. Set Up Environment
   └── python -m venv venv && source venv/bin/activate

3. Install Dependencies
   └── pip install -r requirements.txt

4. Configure Environment
   └── cp .env.example .env
       └── Edit .env with credentials

5. Make Changes
   ├── Edit Python files
   ├── Test locally
   └── Update documentation if needed

6. Commit Changes
   └── git add .
       └── git commit -m "Description"
           └── git push origin main
```

## Future Structure (Potential)

```
FaveNBAHoopers/
├── backend/
│   ├── api/                  # FastAPI or Flask REST API
│   ├── tests/                # Unit and integration tests
│   └── docker/               # Docker configuration
│
├── frontend/                 # React + Tailwind Dashboard
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── hooks/           # Custom hooks
│   │   └── utils/           # Utility functions
│   └── public/              # Static assets
│
├── docs/                    # Extended documentation
└── scripts/                 # Automation scripts
```

## Quick Reference

| Task | Command |
|------|---------|
| First-time setup | `python setup.py` |
| Run ETL pipeline | `python nba_stats_etl.py` |
| Analyze data | `python analyze_stats.py` |
| Install deps | `pip install -r requirements.txt` |
| Create .env | `cp .env.example .env` |
| Activate venv | `source venv/bin/activate` |

## File Size Overview

| File | Lines | Purpose |
|------|-------|---------|
| nba_stats_etl.py | ~220 | Main ETL pipeline |
| config.py | ~60 | Configuration |
| analyze_stats.py | ~180 | Analysis utilities |
| setup.py | ~150 | Setup wizard |
| README.md | ~400 | Main documentation |
| example_queries.sql | ~300 | SQL examples |
| **Total** | ~1,310+ | Production-ready codebase |

---

This structure is designed to be:
- ✅ Easy to understand
- ✅ Easy to maintain
- ✅ Easy to extend
- ✅ Production-ready
- ✅ Well-documented

# Quick Start Guide

Get your NBA stats pipeline up and running in 5 minutes!

## Prerequisites

- Python 3.8+
- PostgreSQL installed and running
- Git (for cloning the repository)

## Installation Steps

### 1. Clone & Navigate

```bash
git clone <your-repo-url>
cd FaveNBAHoopers
```

### 2. Run Setup Wizard (Recommended)

```bash
python setup.py
```

The wizard will:
- Check your Python version
- Install dependencies
- Create your `.env` file
- Create necessary directories
- Test your database connection

### 3. Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

### 4. Configure Database

Edit `.env` with your credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### 5. Run the Pipeline

```bash
python nba_stats_etl.py
```

## What Happens?

1. **Extracts** data from NBA API for 5 players:
   - LeBron James
   - Stephen Curry
   - Damian Lillard
   - Trae Young
   - Giannis Antetokounmpo

2. **Transforms** the data:
   - Adds date components
   - Calculates division/conference
   - Adds home/away indicators
   - Converts percentages

3. **Loads** to PostgreSQL:
   - Individual tables for each player
   - Combined comparison table (`nba_5`)

## Quick Analysis

After running the pipeline, analyze your data:

```bash
python analyze_stats.py
```

This shows:
- Career averages for each player
- Recent form (last 10 games)
- Top scoring performances
- Triple-doubles
- Home vs away splits

## Query the Data

### Using SQL

Connect to your PostgreSQL database and run queries:

```sql
-- Career averages
SELECT 
    player_id,
    COUNT(*) as games,
    ROUND(AVG(pts), 2) as avg_points,
    ROUND(AVG(reb), 2) as avg_rebounds,
    ROUND(AVG(ast), 2) as avg_assists
FROM nba_5
GROUP BY player_id
ORDER BY avg_points DESC;
```

See `example_queries.sql` for 15+ ready-to-use queries!

### Using Python

```python
from analyze_stats import NBAStatsAnalyzer

analyzer = NBAStatsAnalyzer()

# Get career averages
print(analyzer.get_career_averages())

# Get recent form
print(analyzer.get_recent_form(10))

# Get top performances
print(analyzer.get_top_performances('pts', 10))
```

## Next Steps

### 1. Customize Players

Edit `config.py` to add/remove players:

```python
PLAYER_IDS = {
    'lebron_james': 2544,
    'kevin_durant': 201142,  # Add new player
    # ... more players
}
```

### 2. Schedule Regular Updates

Set up a cron job (Linux/Mac) or Task Scheduler (Windows) to run daily:

```bash
# Example cron job - runs daily at 2 AM
0 2 * * * cd /path/to/FaveNBAHoopers && /path/to/venv/bin/python nba_stats_etl.py
```

### 3. Build a Frontend

Create a React + Tailwind dashboard to visualize the data:
- Player comparison charts
- Career progression graphs
- Performance trends
- Head-to-head stats

Check out the README's "Future Enhancements" section for ideas!

## Troubleshooting

### Can't connect to database?

```bash
# Check PostgreSQL is running
psql -U postgres  # Should connect

# Verify credentials in .env
cat .env

# Check database exists
psql -U postgres -c "\l"
```

### Import errors?

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### NBA API rate limiting?

If you see `429 Too Many Requests`, wait a few minutes and try again. The NBA API has rate limits.

## Getting Help

- Check `README.md` for comprehensive documentation
- Review `example_queries.sql` for query inspiration
- See `CHANGELOG.md` for recent changes
- Read `REFACTORING_SUMMARY.md` for technical details

## Resources

- [NBA API Documentation](https://github.com/swar/nba_api)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

Happy analyzing! 🏀📊

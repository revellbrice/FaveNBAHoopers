# NBA Player Stats ETL Pipeline

A Python-based ETL (Extract, Transform, Load) pipeline that collects career statistics for your favorite NBA players using the NBA API and stores them in a PostgreSQL database.

## 🏀 Featured Players

- **LeBron James** - The King
- **Stephen Curry** - Chef Curry
- **Damian Lillard** - Dame Time
- **Trae Young** - Ice Trae
- **Giannis Antetokounmpo** - The Greek Freak

## 📊 Features

- **Automated Data Collection**: Fetches complete career game logs for specified players
- **Data Enrichment**: Adds calculated fields like division, conference, home/away, and date components
- **PostgreSQL Storage**: Organizes data into individual player tables and a combined comparison table
- **Configurable**: Easy to add/remove players via configuration
- **Production-Ready**: Includes error handling, logging, and environment-based configuration

## 🛠️ Tech Stack

- **Python 3.8+**
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM and database toolkit
- **Pandas** - Data manipulation
- **NBA API** - Official NBA statistics

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL database (local or remote)
- pip (Python package manager)

## 🚀 Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd FaveNBAHoopers
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_secure_password
```

### 5. Set Up PostgreSQL Database

Ensure PostgreSQL is running and you have created a database:

```sql
CREATE DATABASE postgres;
```

## 📖 Usage

### Run the ETL Pipeline

```bash
python nba_stats_etl.py
```

The script will:
1. Connect to your PostgreSQL database
2. Fetch career stats for all configured players
3. Transform and enrich the data
4. Create individual tables for each player
5. Create a combined comparison table (`nba_5`)

### Output Tables

The pipeline creates the following tables in your database:

- `lebron_james` - LeBron's complete career stats
- `stephen_curry` - Curry's complete career stats
- `damian_lillard` - Dame's complete career stats
- `trae_young` - Trae's complete career stats
- `giannis_antetokounmpo` - Giannis's complete career stats
- `nba_5` - Combined table with equal games from each player for fair comparison

### Data Schema

Each table includes the following columns:

| Column | Description |
|--------|-------------|
| G | Game number in career |
| Player_ID | Player identifier |
| GAME_DATE | Date of the game |
| MONTH, DAY, YEAR, DAY_OF_WEEK | Date components |
| MATCHUP | Game matchup (e.g., "LAL vs. GSW") |
| LOCATION | HOME or AWAY |
| OPP | Opponent team code |
| DIV | Opponent's division |
| CONF | Opponent's conference |
| WL | Win/Loss |
| MIN | Minutes played |
| FGM, FGA, FG_PCT | Field goals made, attempted, percentage |
| FG3M, FG3A, FG3_PCT | 3-pointers made, attempted, percentage |
| FTM, FTA, FT_PCT | Free throws made, attempted, percentage |
| OREB, DREB, REB | Offensive, defensive, total rebounds |
| AST | Assists |
| STL | Steals |
| BLK | Blocks |
| TOV | Turnovers |
| PF | Personal fouls |
| PTS | Points |
| PLUS_MINUS | Plus/minus rating |

## 🔧 Configuration

### Adding/Removing Players

Edit `config.py` and modify the `PLAYER_IDS` dictionary:

```python
PLAYER_IDS = {
    'player_name': player_id,  # Get player_id from NBA API
    # Add more players here
}
```

To find player IDs, visit: https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/static/players.md

## 📁 Project Structure

```
FaveNBAHoopers/
│
├── nba_stats_etl.py      # Main ETL pipeline script
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT License
└── README.md             # This file
```

## 🔐 Security Notes

- **Never commit your `.env` file** - it contains sensitive credentials
- The `.env.example` file is provided as a template only
- Use strong passwords for your database
- Consider using environment-specific credentials for production

## 🚧 Future Enhancements

### Potential Features

- [ ] Add data validation and quality checks
- [ ] Implement incremental updates (only fetch new games)
- [ ] Add player career statistics summary table
- [ ] Create automated scheduling (e.g., cron job for daily updates)
- [ ] Add unit tests
- [ ] Implement data versioning
- [ ] Add support for playoff vs regular season filtering

### Frontend Visualization (React + Tailwind)

A natural next step would be building a React-based dashboard with Tailwind CSS to visualize this data:

- Interactive player comparison charts
- Career progression visualizations
- Head-to-head statistics
- Performance trend analysis
- Division/Conference performance breakdowns

This would provide hands-on experience with:
- React components and hooks
- Tailwind CSS utility classes
- Chart libraries (Chart.js, Recharts)
- API integration with the PostgreSQL backend
- Responsive design patterns

## 🐛 Troubleshooting

### Database Connection Issues

```
Error: Failed to connect to database
```

**Solution**: Verify your PostgreSQL credentials in `.env` and ensure the database is running.

### NBA API Rate Limiting

```
Error: 429 Too Many Requests
```

**Solution**: The NBA API has rate limits. Add delays between requests or run the script during off-peak hours.

### Missing Dependencies

```
Error: No module named 'nba_api'
```

**Solution**: Ensure you've activated your virtual environment and run `pip install -r requirements.txt`

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [NBA API](https://github.com/swar/nba_api) for providing access to NBA statistics
- NBA for making their data available

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Note**: This project is for educational and personal use only. NBA statistics are property of the NBA.

"""Configuration management for NBA Stats ETL."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration."""
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'postgres')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    
    @property
    def database_url(self):
        """Construct database URL from components."""
        if not self.DB_PASSWORD:
            raise ValueError("DB_PASSWORD environment variable is required")
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Player Configuration
    PLAYER_IDS = {
        'lebron_james': 2544,
        'stephen_curry': 201939,
        'damian_lillard': 203081,
        'trae_young': 1629027,
        'giannis_antetokounmpo': 203507
    }
    
    # NBA Divisions and Conferences
    DIVISIONS = {
        'ATLANTIC': ['BKN', 'PHI', 'TOR', 'BOS', 'NYK', 'NJN'],
        'SOUTHEAST': ['MIA', 'CHA', 'WAS', 'ATL', 'ORL'],
        'CENTRAL': ['CHI', 'CLE', 'MIL', 'IND', 'DET'],
        'PACIFIC': ['PHX', 'GSW', 'LAL', 'LAC', 'SAC', 'GOS', 'PHO'],
        'SOUTHWEST': ['MEM', 'DAL', 'SAS', 'NOP', 'HOU', 'NOH', 'NOK'],
        'NORTHWEST': ['UTA', 'DEN', 'MIN', 'POR', 'OKC', 'SEA']
    }
    
    CONFERENCES = {
        'EASTERN': ['ATLANTIC', 'SOUTHEAST', 'CENTRAL'],
        'WESTERN': ['PACIFIC', 'SOUTHWEST', 'NORTHWEST']
    }
    
    # Project Paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / 'data'
    LOGS_DIR = BASE_DIR / 'logs'

config = Config()

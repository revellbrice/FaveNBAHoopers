"""NBA Stats ETL Pipeline - Extract player stats and load to PostgreSQL."""
import logging
import sys
from typing import Dict, List
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll

from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class NBAStatsETL:
    """ETL pipeline for NBA player statistics."""
    
    def __init__(self):
        """Initialize the ETL pipeline."""
        self.engine = None
        self.player_data = {}
        
    def connect_to_database(self):
        """Establish database connection."""
        try:
            self.engine = create_engine(config.database_url)
            logger.info("Successfully connected to PostgreSQL database")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def extract_player_data(self, player_id: int) -> pd.DataFrame:
        """
        Extract career game log for a specific player.
        
        Args:
            player_id: NBA API player ID
            
        Returns:
            DataFrame containing player's career game log
        """
        try:
            career = playergamelog.PlayerGameLog(
                player_id=player_id,
                season=SeasonAll.all
            )
            df = career.get_data_frames()[0]
            logger.info(f"Extracted {len(df)} games for player {player_id}")
            return df
        except Exception as e:
            logger.error(f"Failed to extract data for player {player_id}: {e}")
            raise
    
    def transform_player_data(self, df: pd.DataFrame, player_name: str) -> pd.DataFrame:
        """
        Transform raw player data with additional features.
        
        Args:
            df: Raw player data DataFrame
            player_name: Name identifier for the player
            
        Returns:
            Transformed DataFrame with additional features
        """
        # Convert date column
        df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
        
        # Sort by game date
        df = df.sort_values(by='GAME_DATE', ascending=True)
        
        # Drop unnecessary columns
        df = df.drop(['SEASON_ID', 'Game_ID', 'VIDEO_AVAILABLE'], axis=1, errors='ignore')
        
        # Convert percentages to more readable format
        df['FG_PCT'] = (df['FG_PCT'] * 100).round(2)
        df['FG3_PCT'] = (df['FG3_PCT'] * 100).round(2)
        df['FT_PCT'] = (df['FT_PCT'] * 100).round(2)
        
        # Add date components
        df['YEAR'] = df['GAME_DATE'].dt.year
        df['MONTH'] = df['GAME_DATE'].dt.month_name()
        df['DAY'] = df['GAME_DATE'].dt.day
        df['DAY_OF_WEEK'] = df['GAME_DATE'].dt.day_name()
        
        # Extract opponent team code
        df['OPP'] = df['MATCHUP'].str[-3:]
        
        # Add division and conference
        df['DIV'] = df['OPP'].apply(self._get_division)
        df['CONF'] = df['OPP'].apply(self._get_conference)
        
        # Add location (home/away)
        df['LOCATION'] = df['MATCHUP'].apply(
            lambda x: 'HOME' if 'vs.' in x else 'AWAY' if '@' in x else ''
        )
        
        # Add game number
        df['G'] = np.arange(1, len(df) + 1)
        
        # Replace Player_ID with name
        df['Player_ID'] = player_name
        
        # Reorder columns for better readability
        column_order = [
            'G', 'Player_ID', 'GAME_DATE', 'MONTH', 'DAY', 'YEAR',
            'DAY_OF_WEEK', 'MATCHUP', 'LOCATION', 'OPP', 'DIV', 'CONF',
            'WL', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT',
            'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL',
            'BLK', 'TOV', 'PF', 'PTS', 'PLUS_MINUS'
        ]
        
        df = df[column_order]
        
        logger.info(f"Transformed data for {player_name}")
        return df
    
    def _get_division(self, team_code: str) -> str:
        """Get division for a team code."""
        for division, teams in config.DIVISIONS.items():
            if team_code in teams:
                return division
        return 'UNKNOWN'
    
    def _get_conference(self, team_code: str) -> str:
        """Get conference for a team code."""
        division = self._get_division(team_code)
        for conference, divisions in config.CONFERENCES.items():
            if division in divisions:
                return conference
        return 'UNKNOWN'
    
    def load_to_database(self, df: pd.DataFrame, table_name: str):
        """
        Load DataFrame to PostgreSQL table.
        
        Args:
            df: DataFrame to load
            table_name: Name of the target table
        """
        try:
            df.to_sql(
                table_name,
                self.engine,
                if_exists='replace',
                index=False
            )
            logger.info(f"Loaded {len(df)} records to table '{table_name}'")
        except Exception as e:
            logger.error(f"Failed to load data to table '{table_name}': {e}")
            raise
    
    def run(self):
        """Execute the full ETL pipeline."""
        try:
            logger.info("Starting NBA Stats ETL Pipeline")
            
            # Connect to database
            self.connect_to_database()
            
            # Extract and transform data for each player
            all_players_data = []
            
            for player_name, player_id in config.PLAYER_IDS.items():
                logger.info(f"Processing {player_name}...")
                
                # Extract
                raw_data = self.extract_player_data(player_id)
                
                # Transform
                transformed_data = self.transform_player_data(raw_data, player_name)
                self.player_data[player_name] = transformed_data
                
                # Load individual player table
                self.load_to_database(transformed_data, player_name)
                
                all_players_data.append(transformed_data)
            
            # Create combined table with equal games for each player
            logger.info("Creating combined player comparison table...")
            min_games = min(len(df) for df in all_players_data)
            
            balanced_data = [df.tail(min_games) for df in all_players_data]
            combined_df = pd.concat(balanced_data, axis=0)
            combined_df = combined_df.sort_values(by='GAME_DATE', ascending=False)
            
            # Load combined table
            self.load_to_database(combined_df, 'nba_5')
            
            logger.info("ETL Pipeline completed successfully!")
            
        except Exception as e:
            logger.error(f"ETL Pipeline failed: {e}")
            raise
        finally:
            if self.engine:
                self.engine.dispose()
                logger.info("Database connection closed")


def main():
    """Main entry point."""
    etl = NBAStatsETL()
    etl.run()


if __name__ == '__main__':
    main()

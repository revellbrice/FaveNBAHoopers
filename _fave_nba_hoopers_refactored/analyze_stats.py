"""
Quick data analysis utilities for NBA stats.

This module provides simple functions to analyze the data without writing SQL.
"""
import pandas as pd
from sqlalchemy import create_engine
from config import config


class NBAStatsAnalyzer:
    """Helper class for analyzing NBA player statistics."""
    
    def __init__(self):
        """Initialize the analyzer with database connection."""
        self.engine = create_engine(config.database_url)
    
    def get_career_averages(self) -> pd.DataFrame:
        """Get career averages for all players."""
        query = """
        SELECT 
            player_id,
            COUNT(*) as games_played,
            ROUND(AVG(pts), 2) as avg_points,
            ROUND(AVG(reb), 2) as avg_rebounds,
            ROUND(AVG(ast), 2) as avg_assists,
            ROUND(AVG(stl), 2) as avg_steals,
            ROUND(AVG(blk), 2) as avg_blocks,
            ROUND(AVG(fg_pct), 2) as avg_fg_pct,
            ROUND(AVG(fg3_pct), 2) as avg_3pt_pct
        FROM nba_5
        GROUP BY player_id
        ORDER BY avg_points DESC
        """
        return pd.read_sql(query, self.engine)
    
    def get_player_data(self, player_name: str) -> pd.DataFrame:
        """
        Get all data for a specific player.
        
        Args:
            player_name: Name of the player (e.g., 'lebron_james')
            
        Returns:
            DataFrame with all player data
        """
        return pd.read_sql_table(player_name, self.engine)
    
    def get_top_performances(self, stat: str = 'pts', limit: int = 10) -> pd.DataFrame:
        """
        Get top performances by a specific stat.
        
        Args:
            stat: Statistic to rank by (pts, reb, ast, etc.)
            limit: Number of results to return
            
        Returns:
            DataFrame with top performances
        """
        query = f"""
        SELECT 
            player_id,
            game_date,
            matchup,
            pts, reb, ast, stl, blk,
            fg_pct, fg3_pct
        FROM nba_5
        ORDER BY {stat} DESC
        LIMIT {limit}
        """
        return pd.read_sql(query, self.engine)
    
    def compare_players(self, stats: list = None) -> pd.DataFrame:
        """
        Compare all players across specified stats.
        
        Args:
            stats: List of stats to compare (default: pts, reb, ast)
            
        Returns:
            DataFrame with player comparisons
        """
        if stats is None:
            stats = ['pts', 'reb', 'ast']
        
        stat_calcs = ', '.join([f'ROUND(AVG({s}), 2) as avg_{s}' for s in stats])
        
        query = f"""
        SELECT 
            player_id,
            COUNT(*) as games,
            {stat_calcs}
        FROM nba_5
        GROUP BY player_id
        ORDER BY avg_{stats[0]} DESC
        """
        return pd.read_sql(query, self.engine)
    
    def get_recent_form(self, games: int = 10) -> pd.DataFrame:
        """
        Get recent form for all players.
        
        Args:
            games: Number of recent games to analyze
            
        Returns:
            DataFrame with recent performance stats
        """
        query = f"""
        WITH recent_games AS (
            SELECT 
                player_id,
                game_date,
                pts, reb, ast, wl,
                ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY game_date DESC) as game_rank
            FROM nba_5
        )
        SELECT 
            player_id,
            ROUND(AVG(pts), 2) as avg_points_last_{games},
            ROUND(AVG(reb), 2) as avg_rebounds_last_{games},
            ROUND(AVG(ast), 2) as avg_assists_last_{games},
            SUM(CASE WHEN wl = 'W' THEN 1 ELSE 0 END) as wins_last_{games}
        FROM recent_games
        WHERE game_rank <= {games}
        GROUP BY player_id
        ORDER BY avg_points_last_{games} DESC
        """
        return pd.read_sql(query, self.engine)
    
    def get_triple_doubles(self) -> pd.DataFrame:
        """Get all triple-double games."""
        query = """
        SELECT 
            player_id,
            game_date,
            matchup,
            pts, reb, ast, stl, blk
        FROM nba_5
        WHERE pts >= 10 AND reb >= 10 AND ast >= 10
        ORDER BY game_date DESC
        """
        return pd.read_sql(query, self.engine)
    
    def home_vs_away(self) -> pd.DataFrame:
        """Compare home vs away performance."""
        query = """
        SELECT 
            player_id,
            location,
            COUNT(*) as games,
            ROUND(AVG(pts), 2) as avg_points,
            ROUND(AVG(reb), 2) as avg_rebounds,
            ROUND(AVG(ast), 2) as avg_assists,
            ROUND(AVG(fg_pct), 2) as avg_fg_pct,
            ROUND(SUM(CASE WHEN wl = 'W' THEN 1 ELSE 0 END)::FLOAT / COUNT(*) * 100, 2) as win_pct
        FROM nba_5
        WHERE location IN ('HOME', 'AWAY')
        GROUP BY player_id, location
        ORDER BY player_id, location
        """
        return pd.read_sql(query, self.engine)


def main():
    """Example usage of the analyzer."""
    analyzer = NBAStatsAnalyzer()
    
    print("=" * 60)
    print("NBA STATS QUICK ANALYSIS")
    print("=" * 60)
    
    # Career averages
    print("\n📊 Career Averages:")
    print(analyzer.get_career_averages().to_string(index=False))
    
    # Recent form
    print("\n🔥 Recent Form (Last 10 Games):")
    print(analyzer.get_recent_form(10).to_string(index=False))
    
    # Top scoring performances
    print("\n🏀 Top 5 Scoring Performances:")
    print(analyzer.get_top_performances('pts', 5)[
        ['player_id', 'game_date', 'matchup', 'pts', 'reb', 'ast']
    ].to_string(index=False))
    
    # Triple doubles
    triple_doubles = analyzer.get_triple_doubles()
    print(f"\n⭐ Triple-Doubles: {len(triple_doubles)} total")
    if len(triple_doubles) > 0:
        print(triple_doubles.head()[
            ['player_id', 'game_date', 'matchup', 'pts', 'reb', 'ast']
        ].to_string(index=False))
    
    # Home vs Away
    print("\n🏠 Home vs Away Performance:")
    print(analyzer.home_vs_away().to_string(index=False))


if __name__ == '__main__':
    main()

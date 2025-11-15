-- Example SQL Queries for NBA Stats Analysis
-- ============================================

-- 1. Get career averages for each player
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
ORDER BY avg_points DESC;


-- 2. Best scoring performances (top 10 games)
SELECT 
    player_id,
    game_date,
    matchup,
    pts as points,
    reb as rebounds,
    ast as assists
FROM nba_5
ORDER BY pts DESC
LIMIT 10;


-- 3. Home vs Away performance comparison
SELECT 
    player_id,
    location,
    COUNT(*) as games,
    ROUND(AVG(pts), 2) as avg_points,
    ROUND(AVG(fg_pct), 2) as avg_fg_pct,
    SUM(CASE WHEN wl = 'W' THEN 1 ELSE 0 END)::FLOAT / COUNT(*) * 100 as win_pct
FROM nba_5
WHERE location IN ('HOME', 'AWAY')
GROUP BY player_id, location
ORDER BY player_id, location;


-- 4. Performance by day of week
SELECT 
    player_id,
    day_of_week,
    COUNT(*) as games,
    ROUND(AVG(pts), 2) as avg_points,
    ROUND(AVG(fg_pct), 2) as avg_fg_pct
FROM nba_5
GROUP BY player_id, day_of_week
ORDER BY player_id, 
    CASE day_of_week
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END;


-- 5. Conference performance (Eastern vs Western)
SELECT 
    player_id,
    conf as conference,
    COUNT(*) as games,
    ROUND(AVG(pts), 2) as avg_points,
    ROUND(AVG(reb), 2) as avg_rebounds,
    ROUND(AVG(ast), 2) as avg_assists,
    SUM(CASE WHEN wl = 'W' THEN 1 ELSE 0 END)::FLOAT / COUNT(*) * 100 as win_pct
FROM nba_5
GROUP BY player_id, conf
ORDER BY player_id, conf;


-- 6. Recent form (last 10 games per player)
WITH recent_games AS (
    SELECT 
        player_id,
        game_date,
        pts,
        reb,
        ast,
        wl,
        ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY game_date DESC) as game_rank
    FROM nba_5
)
SELECT 
    player_id,
    ROUND(AVG(pts), 2) as avg_points_last_10,
    ROUND(AVG(reb), 2) as avg_rebounds_last_10,
    ROUND(AVG(ast), 2) as avg_assists_last_10,
    SUM(CASE WHEN wl = 'W' THEN 1 ELSE 0 END) as wins_last_10
FROM recent_games
WHERE game_rank <= 10
GROUP BY player_id
ORDER BY avg_points_last_10 DESC;


-- 7. Triple-double games
SELECT 
    player_id,
    game_date,
    matchup,
    pts,
    reb,
    ast,
    stl,
    blk
FROM nba_5
WHERE pts >= 10 
  AND reb >= 10 
  AND ast >= 10
ORDER BY game_date DESC;


-- 8. 30+ point games count
SELECT 
    player_id,
    COUNT(*) as games_30plus_points,
    ROUND(AVG(pts), 2) as avg_in_30plus_games
FROM nba_5
WHERE pts >= 30
GROUP BY player_id
ORDER BY games_30plus_points DESC;


-- 9. Performance by month
SELECT 
    player_id,
    month,
    COUNT(*) as games,
    ROUND(AVG(pts), 2) as avg_points,
    ROUND(AVG(fg_pct), 2) as avg_fg_pct,
    ROUND(AVG(fg3_pct), 2) as avg_3pt_pct
FROM nba_5
GROUP BY player_id, month
ORDER BY player_id, 
    CASE month
        WHEN 'January' THEN 1
        WHEN 'February' THEN 2
        WHEN 'March' THEN 3
        WHEN 'April' THEN 4
        WHEN 'May' THEN 5
        WHEN 'June' THEN 6
        WHEN 'July' THEN 7
        WHEN 'August' THEN 8
        WHEN 'September' THEN 9
        WHEN 'October' THEN 10
        WHEN 'November' THEN 11
        WHEN 'December' THEN 12
    END;


-- 10. Most efficient scoring games (high points on high FG%)
SELECT 
    player_id,
    game_date,
    matchup,
    pts,
    fgm,
    fga,
    fg_pct,
    fg3m,
    fg3a,
    fg3_pct
FROM nba_5
WHERE pts >= 25 
  AND fg_pct >= 50
ORDER BY pts DESC, fg_pct DESC
LIMIT 20;


-- 11. Year-over-year career progression for a specific player
-- (Replace 'lebron_james' with any player name)
SELECT 
    year,
    COUNT(*) as games_played,
    ROUND(AVG(pts), 2) as avg_points,
    ROUND(AVG(reb), 2) as avg_rebounds,
    ROUND(AVG(ast), 2) as avg_assists,
    ROUND(AVG(fg_pct), 2) as avg_fg_pct,
    ROUND(AVG(fg3_pct), 2) as avg_3pt_pct,
    SUM(CASE WHEN wl = 'W' THEN 1 ELSE 0 END)::FLOAT / COUNT(*) * 100 as win_pct
FROM lebron_james
GROUP BY year
ORDER BY year;


-- 12. Head-to-head matchup stats (against specific opponent)
-- Example: Performance against the Warriors (GSW)
SELECT 
    player_id,
    COUNT(*) as games_vs_gsw,
    ROUND(AVG(pts), 2) as avg_points,
    ROUND(AVG(reb), 2) as avg_rebounds,
    ROUND(AVG(ast), 2) as avg_assists,
    SUM(CASE WHEN wl = 'W' THEN 1 ELSE 0 END)::FLOAT / COUNT(*) * 100 as win_pct
FROM nba_5
WHERE opp = 'GSW'
GROUP BY player_id
ORDER BY avg_points DESC;


-- 13. Clutch performance (games decided by 5 points or less)
SELECT 
    player_id,
    COUNT(*) as close_games,
    ROUND(AVG(pts), 2) as avg_points,
    ROUND(AVG(ast), 2) as avg_assists,
    SUM(CASE WHEN wl = 'W' THEN 1 ELSE 0 END)::FLOAT / COUNT(*) * 100 as win_pct_close_games
FROM nba_5
WHERE ABS(plus_minus) <= 5
GROUP BY player_id
ORDER BY win_pct_close_games DESC;


-- 14. Career milestones
SELECT 
    player_id,
    MIN(game_date) as first_game,
    MAX(game_date) as most_recent_game,
    COUNT(*) as total_games,
    SUM(pts) as career_points,
    SUM(reb) as career_rebounds,
    SUM(ast) as career_assists,
    MAX(pts) as career_high_points
FROM nba_5
GROUP BY player_id
ORDER BY career_points DESC;


-- 15. Consistency analysis (standard deviation of points)
SELECT 
    player_id,
    COUNT(*) as games,
    ROUND(AVG(pts), 2) as avg_points,
    ROUND(STDDEV(pts), 2) as stddev_points,
    ROUND(MIN(pts), 2) as min_points,
    ROUND(MAX(pts), 2) as max_points
FROM nba_5
GROUP BY player_id
ORDER BY stddev_points ASC;

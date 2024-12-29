import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Get a connection to the database."""
    DATABASE_URL = os.getenv('DATABASE_URL')
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def get_teams():
    """Get list of all teams."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Get unique teams from QB stats as a representative table
            cur.execute("""
                SELECT DISTINCT team 
                FROM qb_stats 
                ORDER BY team
            """)
            return [row['team'] for row in cur.fetchall()]

def get_players_by_position(position: str):
    """Get all players for a specific position."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            table_name = f"{position.lower()}_stats"
            cur.execute(f"""
                SELECT playerid, playername, team 
                FROM {table_name}
                ORDER BY totalpoints DESC
            """)
            return cur.fetchall()

def get_players_by_team(team: str):
    """Get all players for a specific team."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Query each position table and combine results
            players = []
            position_tables = ['qb_stats', 'rb_stats', 'wr_stats', 'te_stats', 'k_stats', 'db_stats', 'dl_stats', 'lb_stats']
            
            for table in position_tables:
                cur.execute(f"""
                    SELECT 
                        playerid, 
                        playername, 
                        team,
                        '{table.split('_')[0].upper()}' as position
                    FROM {table}
                    WHERE UPPER(team) = UPPER(%s)
                    ORDER BY totalpoints DESC
                """, (team,))
                players.extend(cur.fetchall())
            
            return players

def get_position_stats(position: str):
    """Get detailed statistics for a position."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            table_name = f"{position.lower()}_stats"
            try:
                cur.execute(f"""
                    SELECT *
                    FROM {table_name}
                    ORDER BY totalpoints DESC
                """)
                results = cur.fetchall()
                if not results:
                    return []
                return results
            except psycopg2.Error as e:
                print(f"Database error: {e}")
                raise Exception(f"Error fetching stats for position {position}")

def get_team_points(team: str):
    """Get total points for a team."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Sum points from all position tables
            total_points = 0
            position_tables = ['qb_stats', 'rb_stats', 'wr_stats', 'te_stats', 'k_stats', 'db_stats', 'dl_stats', 'lb_stats']
            
            for table in position_tables:
                cur.execute(f"""
                    SELECT COALESCE(SUM(totalpoints), 0) as points
                    FROM {table}
                    WHERE UPPER(team) = UPPER(%s)
                """, (team,))
                result = cur.fetchone()
                total_points += float(result['points']) if result['points'] else 0
            
            return total_points 
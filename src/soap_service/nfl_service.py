from spyne import Application, rpc, ServiceBase, Unicode, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.model.complex import ComplexModel
from spyne.model.primitive import Integer, Decimal
import sys
from pathlib import Path

# Add the src directory to the Python path
src_dir = str(Path(__file__).parent.parent)
if src_dir not in sys.path:
    sys.path.append(src_dir)

from database.queries import (
    get_teams,
    get_players_by_position,
    get_players_by_team,
    get_position_stats,
    get_team_points
)

class PlayerStats(ComplexModel):
    """Player statistics complex type"""
    totalpoints = Decimal
    # QB Stats
    passingyards = Integer(min_occurs=0)
    passingtds = Integer(min_occurs=0)
    interceptions = Integer(min_occurs=0)
    # WR/TE Stats
    receptions = Integer(min_occurs=0)
    targets = Integer(min_occurs=0)
    receivingyards = Integer(min_occurs=0)
    receivingtds = Integer(min_occurs=0)
    # Defensive Stats
    tackles = Integer(min_occurs=0)
    sacks = Decimal(min_occurs=0)
    tackles_tfl = Integer(min_occurs=0)
    # Kicker Stats
    fieldgoals = Integer(min_occurs=0)
    fieldgoalattempts = Integer(min_occurs=0)
    extrapoints = Integer(min_occurs=0)
    extrapointattempts = Integer(min_occurs=0)

class Player(ComplexModel):
    """Player complex type"""
    playerid = Unicode
    playername = Unicode
    team = Unicode
    position = Unicode
    stats = PlayerStats

class NFLStatsService(ServiceBase):
    @rpc(Unicode, _returns=Array(Player))
    def get_players_by_position(ctx, position):
        """Get players by position"""
        if position not in ["QB", "RB", "WR", "TE", "K", "DB", "DL", "LB"]:
            raise ValueError(f"Invalid position: {position}")
        
        players = get_players_by_position(position.upper())
        return [Player(
            playerid=p['playerid'],
            playername=p['playername'],
            team=p.get('team', 'Unknown'),
            position=position,
            stats=None
        ) for p in players if p.get('playername')]

    @rpc(Unicode, _returns=Array(Player))
    def get_position_stats(ctx, position):
        """Get detailed statistics for a position"""
        if position not in ["QB", "RB", "WR", "TE", "DB", "DL", "LB", "K"]:
            raise ValueError(f"Invalid position: {position}")
        
        stats = get_position_stats(position.upper())
        return [Player(
            playerid=s['playerid'],
            playername=s['playername'],
            team=s.get('team', 'Unknown'),
            position=position,
            stats=PlayerStats(**{k: float(v) if v is not None else 0 
                               for k, v in s.items() 
                               if k not in ['playerid', 'playername', 'team', 'position']})
        ) for s in stats]

    @rpc(_returns=Array(Unicode))
    def get_teams(ctx):
        """Get all teams"""
        return get_teams()

    @rpc(Unicode, _returns=Decimal)
    def get_team_points(ctx, team):
        """Get total points for a team"""
        return Decimal(str(get_team_points(team.upper())))

application = Application([NFLStatsService],
    tns='http://nfl.stats/soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_application = WsgiApplication(application) 
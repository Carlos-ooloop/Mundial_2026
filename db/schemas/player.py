from db.models.players import Position
def player_schema(player)-> dict:
    return {"id": str(player["_id"]),
            "name":player.get("name"), 
            "sur_name":player.get( "sur_name"),
            "age":player.get("age"),
            "position":Position(player.get("position")),
            "club":player.get("club"),
            "national_team":player.get("national_team"),
            "goals":player.get("goals"),
            "assits":player.get("assits"),
            "goal_contributions":player.get("goal_contributions"),
            "clean_sheets":player.get("clean_sheets"),
            "tackles":player.get("tackles"),
            "shots": player.get("shots"),
            "shots_on_target":player.get("shots_on_target"),
            "interceptions":player.get("interceptions"),
            "saves": player.get("saves"),
             }
 
 
def players_schemas(players)->list:
     return [player_schema(player) for player in players]   
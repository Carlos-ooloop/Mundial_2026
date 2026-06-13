def selection_schema(selection)->dict:
    return {"id":str(selection["_id"]),
            "name":selection.get("name"),
            "coach":selection.get("coach"),
            "ranking_fifa":selection.get("ranking_fifa")}
    
def selection_schemas(selections)->list:
    return [selection_schema(selection) for selection in selections ]    
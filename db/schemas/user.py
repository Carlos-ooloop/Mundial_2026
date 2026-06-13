def user_schema(user) -> dict:
    return {"id":str(user.get("_id")),
            "username":user.get( "username"),
            "email":user["email"],
             "password": user.get("password"),
             "role":user.get("role")}
def users_schemas(users) -> list:
    return  [ user_schema(user) for user in users ]  


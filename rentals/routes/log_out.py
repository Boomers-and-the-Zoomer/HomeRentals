from bottle import post, response


@post("/log-out")
def log_out():
    response.delete_cookie("Session")
    response.status = 303
    response.add_header("Location", "/")
    # FIXME: Actually delete the session from the db

import werkzeug.exceptions


class BadRequest(werkzeug.exceptions.HTTPException):
    code = 400

    def __init__(self, description: str = "Bad Request"):
        self.description = description
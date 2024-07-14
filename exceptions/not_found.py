import werkzeug.exceptions


class NotFound(werkzeug.exceptions.HTTPException):
    code = 404

    def __init__(self, description: str = "Not Found"):
        self.description = description

from werkzeug.exceptions import BadRequest


class RoomsNotFound(BadRequest):
    pass

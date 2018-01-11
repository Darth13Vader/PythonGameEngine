

class PGENotInitializedError(BaseException):
    def __init__(self):
        self.args = ('Python Game Engine hasn`t been initialized yet')
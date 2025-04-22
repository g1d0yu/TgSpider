class SingletonId(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonId, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class UserInfo(metaclass=SingletonId):

    def __init__(self, user_id):
        self.user_id = user_id

    def get_userid(self):
        return self.user_id




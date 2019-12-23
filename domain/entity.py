class Entity:

    def __init__(self):
        self._id = None

    def get_id(self):
        return self._id

    def set_id(self, _id):
        self._id = _id

    def __repr__(self):
        to_str = {}

        for key, value in self.__dict__.items():
            if type(value) == list:
                to_str[key] = len(value)
            elif key.startswith('geo'):
                to_str[key] = value[:10] + '...'
            else:
                to_str[key] = value

        return str(to_str)

import abc


class ModelLoader(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def load_resource(self, resource):
        return

from abc import ABCMeta, abstractmethod


class Model(metaclass=ABCMeta):
    @abstractmethod
    def json(self):
        raise NotImplementedError

    @abstractmethod
    def save_to_db(self):
        raise NotImplementedError

    @abstractmethod
    def delete_from_db(self):
        raise NotImplementedError

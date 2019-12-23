import abc
import threading


class ConnectionHolder:
    def __init__(self, provider, close_on_release=True):
        self.provider = provider
        self.close_on_release = close_on_release
        self.__conn = None
        self.released = False

    def connect(self):
        if self.__conn is None:
            self.__conn = self.provider.create_connection()
        return self.__conn

    def release(self):
        self.provider._realease_holder(self)

    def _close(self):
        if self.close_on_release:
            self._force_close()
        self.released = True

    def _force_close(self):
        if self.__conn is not None:
            self.__conn.close()
            self.__conn = None
        self.released = True

    def is_released(self):
        return self.released


class ConnectionProvider(metaclass=abc.ABCMeta):

    def __init__(self):
        self.holders = []
        self.__holders_lock = threading.Lock()

    @abc.abstractmethod
    def create_connection(self):
        return

    def get_holder(self, close_on_release=False):
        with self.__holders_lock:
            free_holders = self.__find_released_holder()

            if len(free_holders) > 0:
                return free_holders[0]
            return self.__create_holder(close_on_release)

    def __find_released_holder(self):
        return [h for h in self.holders if h.is_released()]

    def __create_holder(self, close_on_release):
        holder = ConnectionHolder(self, close_on_release)
        self.holders.append(holder)
        return holder

    def _realease_holder(self, holder):
        with self.__holders_lock:
            holder._close()

    def close_all_holders(self):
        with self.__holders_lock:
            for holder in self.holders[:]:
                holder._force_close()
                self.holders.remove(holder)

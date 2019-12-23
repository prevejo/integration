import psycopg2

from db.connection_provider import ConnectionProvider


class DataBase(ConnectionProvider):
    def __init__(self, host, db_name, user, password, has_postgis_extension=False):
        super(DataBase, self).__init__()
        self.host = host
        self.db_name = db_name
        self.user = user
        self.password = password
        self.has_postgis_extension = has_postgis_extension

    def create_connection(self):
        return psycopg2.connect(host=self.host, database=self.db_name, user=self.user, password=self.password)

    @staticmethod
    def instance_output_db():
        return DataBase('localhost', 'prevejodb', 'postgres', 'postgres', True)


class Query:
    def __init__(self, query):
        self.query = query

    def fetch(self, return_type, conn_holder):
        conn = conn_holder.connect()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(self.query)
                rs = cursor.fetchall()

                columns = [desc[0] for desc in cursor.description]
                attributes = [attr[1] for attr in return_type.__init__.__annotations__.items()]

                lines = [self.__parse(line, columns, attributes) for line in rs]

                return [return_type(*tuple(line)) for line in lines]
            finally:
                cursor.close()
        finally:
            conn_holder.release()

    def fetchall(self, consumer, conn_holder):
        conn = conn_holder.connect()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(self.query)
                return consumer(cursor.fetchall())
            finally:
                cursor.close()
        finally:
            conn_holder.release()

    @staticmethod
    def __parse(line, columns, attrs):
        ret_list = []
        for attr in attrs:
            index = columns.index(attr)
            if index == -1:
                ret_list.append(None)
            else:
                ret_list.append(line[index])
        return ret_list

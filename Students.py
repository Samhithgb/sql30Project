from sql30 import db
import psycopg2


class Students(db.Model):
    TABLE = "students"
    P_KEY = "id"

    def init_connection(self):
        self.verbose = True
        print("Init connection")
        if not self._conn:
            print("Init connection : Connection null")

            self._conn = psycopg2.connect(
                host="localhost",
                database="sql30",
                user="postgres",
                password="vmware")

            self._cursor = self._conn.cursor()

    def __enter__(self):
        assert not self._context_conn, "nested context not allowed"
        self._context_conn = psycopg2.connect(
            host="localhost",
            database="sql30",
            user="postgres",
            password="vmware")

        self._context_cursor = self._context_conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._context_conn:
            self._context_conn.commit()
            self._context_conn.close()
            self._context_conn = None
            self._context_cursor = None

    def table_exists(self, tbl_name):
        self.verbose = True

        self._cursor.execute("select * from information_schema.tables where table_name=%s", (tbl_name,))
        print("Table exists? " + str(bool(self._cursor.rowcount)))
        return bool(self._cursor.rowcount)

    def create(self, tbl=None, **kwargs):
        tbl = tbl or self.table
        assert tbl, "No table set for operation"
        self._validate_bfr_write(tbl, kwargs)

        values = [kwargs.get(field, '') for field in self._get_fields(tbl)]

        cmnd = 'INSERT INTO %s VALUES (%s)' % (tbl, ','.join(['%s'] * len(values)))
        values = tuple(values)
        self.cursor.execute(cmnd,values )

    DB_SCHEMA = {
        'db_name': './sql30.db',
        'tables': [
            {
                'name': TABLE,
                'fields': {
                    'id': 'int',
                    'name': 'text',
                    'marks': 'int',
                    'fees': 'text'
                },
                'primary_key': P_KEY
            }]
    }
    VALIDATE_BEFORE_WRITE = True

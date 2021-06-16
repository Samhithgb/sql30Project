from sql30 import db


class Students(db.Model):
    TABLE = "STUDENTS"
    P_KEY = "id"

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

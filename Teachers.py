from sql30 import db


class Teachers(db.Model):
    TABLE = "teachers"
    P_KEY = "id"

    DB_SCHEMA = {
        'db_name': './Teachers.db',
        'tables': [
            {
                'name': TABLE,
                'fields': {
                    'id': 'int',
                    'name': 'text',
                    'subject': 'int'
                },
                'primary_key': P_KEY
            }]
    }
    VALIDATE_BEFORE_WRITE = True

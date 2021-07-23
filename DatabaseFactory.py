import Teachers
import Students


def get_database(db="student"):
    database = {
        "teacher": Teachers.Teachers(),
        "students": Students.Students()
    }
    return database[db]

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import DatabaseFactory
import os

import Students
import Teachers


def access_database():
    with DatabaseFactory.get_database("students") as db:
        db.table = 'students'
        db.create(id=2, name="Samhith", marks="100", fees = "1000")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    access_database()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

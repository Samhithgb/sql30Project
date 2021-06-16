# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import DatabaseFactory
import os


def access_database():
    teacher = DatabaseFactory.get_database("teacher")
    teacher.tbl = 'TEACHERS'
    teacher.write(id=1, name="Samhith", subject="Subject")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    access_database()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

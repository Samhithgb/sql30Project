# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import DatabaseFactory
import os

import SharedResource
import Students
import Teachers
import MyThread

def access_database():
    with DatabaseFactory.get_database("students") as db:
        db.table = 'students'
        db.create(id=2, name="Samhith", marks="100", fees="1000")


# Press the green button in the gutter to run the script.
def run_threads():

    work_list = ["Work1", "Work2", "Work3", "Work4", "Work5"]

    shared_resource = SharedResource.SharedResource()

    thread1 = MyThread.MyThread(1, "Thread1", 10,shared_resource )
    thread2 = MyThread.MyThread(1, "Thread2", 10, shared_resource)

    for i in work_list:
        shared_resource.add_work(i)

    thread1.start()
    thread2.start()

    threads = []

    threads.append(thread1)
    threads.append(thread2)

    for i in threads:
        i.join()

    print("Done")

if __name__ == '__main__':
    # access_database()
    run_threads()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

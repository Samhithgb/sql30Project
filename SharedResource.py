import threading
import time
import queue


class SharedResource:
    def __init__(self):
        self.lock = threading.Lock()
        self.cause_for_race = 0
        self.work_queue = queue.Queue(10)

    def add_work(self, work: str):
        self.lock.acquire(True)

        self.work_queue.put(work)
        print("Added work %s" % work)

        self.lock.release()

    def print(self, thread_name):
        self.lock.acquire(True)
        try:
            self.cause_for_race = self.cause_for_race + 1
            print("%s is accessing now. New value : %s" % (thread_name, self.cause_for_race))

            next_work = self.work_queue.get(True, 2)
            print("Work taken by %s : %s" % (thread_name, next_work))

            time.sleep(2)  # sleep for 2 seconds before releasing the lock.

        except queue.Empty:
            print("Queue is empty : Releasing lock now")


        finally:

            self.lock.release()

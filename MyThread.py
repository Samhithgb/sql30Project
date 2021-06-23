import time
import threading
import SharedResource


class MyThread(threading.Thread):

    def __init__(self, thread_id, thread_name, counter, shared_resource: SharedResource):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.counter = counter
        self.shared_resource = shared_resource

    def run(self) -> None:
        print("Running %s with id: %s" % (self.thread_name, self.thread_id))
        while self.counter:
            self.counter = self.counter - 1
            self.shared_resource.print(self.thread_name)
            time.sleep(1)

import pali.task
from pali import worker, task, logger
import SharedResource
import time


class PaliTask(pali.task.Task):

    def __init__(self, thread_id, thread_name, counter, shared_resource: SharedResource):
        self.thread_id = thread_id
        self.shared_resource = shared_resource
        self.done = False
        self.counter = counter
        self.thread_name = "Pali_" + thread_name

    def _run(self):
        print("Running Pali Task %s with id: %s" % (self.thread_name, self.thread_id))
        while self.counter:
            self.counter = self.counter - 1
            self.shared_resource.print(self.thread_name)
            time.sleep(1)

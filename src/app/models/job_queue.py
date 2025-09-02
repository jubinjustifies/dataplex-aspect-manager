from collections import deque


class JobQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, job):
        self.queue.append(job)

    def dequeue(self):
        if self.queue:
            return self.queue.popleft()
        return None

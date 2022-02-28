# Implementation of linear queue
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
         return len(self.items) == 0

    def enqueue(self, newItem):
        self.items.append(newItem)

    def dequeue(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)
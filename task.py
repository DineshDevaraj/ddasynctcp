
from typing import Generator

class Task:

    taskId: int = 0

    def __init__(self, target: Generator) -> None:

        Task.taskId += 1
        self.taskId = Task.taskId
        self.target = target
        self.arg = None

    def run(self):

        return self.target.send(self.arg)


from abc import ABC
from abc import abstractmethod
from typing import Generator

class SystemCall(ABC):

    @abstractmethod
    def handle(self):
        pass

class GetTaskId(SystemCall):

    def handle(self):
        self.task.arg = self.task.taskId
        self.sched.schedule(self.task)

class CreateTask(SystemCall):

    def __init__(self, target: Generator) -> None:
        self.target = target

    def handle(self):
        taskId = self.sched.new(self.target)
        self.sched.schedule(self.task)
        self.task.arg = taskId
        self.taskId = taskId

class KillTask(SystemCall):

    def __init__(self, taskId: int) -> None:
        self.taskId = taskId

    def handle(self):
        self.task.arg = False
        task = self.sched.get_task(self.taskId)
        if task:
            task.target.close()
            self.task.arg = True        
        self.sched.schedule(self.task)

class WaitForTask(SystemCall):

    def __init__(self, waitOnTaskId) -> None:
        self.waitOnTaskId = waitOnTaskId

    def handle(self):
        result: bool = self.sched.at_exit(self.task, self.waitOnTaskId)
        if not result:
            self.sched.schedule(self.task)
        self.task.arg = result

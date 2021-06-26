
from task import Task
from queue import Queue
from typing import Generator
from syscall import SystemCall

class Scheduler:

    def __init__(self) -> None:

        self.waitForExit = {}
        self.ready = Queue()
        self.taskmap = {}

    def new(self, target: Generator):

        task = Task(target)
        self.taskmap[task.taskId] = task
        self.schedule(task)
        return task.taskId

    def schedule(self, task: Task):

        self.ready.put(task)

    def exit(self, task: Task):

        print(f"terminated task {task.taskId}")
        del self.taskmap[task.taskId]
        taskList = self.waitForExit.pop(task.taskId, None)
        if taskList is None: return
        for task in taskList: self.schedule(task)

    def start(self):

        while self.taskmap:

            task: Task = self.ready.get()

            try:
                result = task.run()
                if isinstance(result, SystemCall):
                    result.task = task
                    result.sched = self
                    result.handle()
                    continue
            except StopIteration:
                self.exit(task)
                continue

            self.ready.put(task)

    def get_task(self, taskId: int):
        return self.taskmap.get(taskId, None)

    def at_exit(self, notifyTask, waitOnTaskId) -> bool:

        if waitOnTaskId not in self.taskmap:
            return False

        taskList = self.waitForExit.get(waitOnTaskId, None)
        if taskList is None:
            taskList = self.waitForExit[waitOnTaskId] = []
        taskList.append(notifyTask)

        return True

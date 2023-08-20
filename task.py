
from collections import deque
from syscall import SystemCall
from typing import Generator

class Task:

    taskId: int = 0

    def __init__(self, target: Generator) -> None:

        Task.taskId += 1
        self.stack = deque()
        self.taskId = Task.taskId
        self.target = target
        self.arg = None

    def run(self):

        while True:
                
            try :

                result = self.target.send(self.arg)

                if isinstance(result, SystemCall):
                    return result

                if isinstance(result, Generator):

                    self.stack.append(self.target)
                    self.target = result
                    self.arg = None

                else:

                    if not self.stack: 
                        return

                    self.target = self.stack.pop()
                    self.arg = result

            except StopIteration:

                if not self.stack:
                    raise

                self.target = self.stack.pop()
                self.arg = None

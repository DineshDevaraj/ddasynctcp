
from syscall import CreateTask, GetTaskId, KillTask, WaitForTask
from scheduler import Scheduler

def counter(maxLimit: int):
    tid = yield GetTaskId()
    for I in range(maxLimit):
        print(f"Task {tid} {I}")
        yield

def multiple_couroutines():

    scheduler = Scheduler()
    scheduler.new(counter(10))
    scheduler.new(counter(5))
    scheduler.start()

def nested_couroutines():

    selfId = yield GetTaskId()
    taskId = yield CreateTask(counter(10))
    for x in range(5):
        print(f"Task {selfId} {x}")
        yield
    yield WaitForTask(taskId)
    yield KillTask(taskId)

if __name__ == "__main__":
    
    sched = Scheduler()
    sched.new(nested_couroutines())
    sched.start()

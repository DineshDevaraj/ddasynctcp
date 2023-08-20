
from syscall import CreateTask, GetTaskId, KillTask, WaitForTask
from scheduler import Scheduler

def counter(maxLimit: int):
    tid = yield GetTaskId()
    for I in range(maxLimit):
        print(f"Task {tid} {I}")
        yield

def multiple_couroutines(sched):

    sched.new(counter(10))
    sched.new(counter(5))

def syscall_couroutines():

    selfId = yield GetTaskId()
    taskId = yield CreateTask(counter(10))
    for x in range(5):
        print(f"Task {selfId} {x}")
        yield
    yield WaitForTask(taskId)
    yield KillTask(taskId)

def coroutine_level2():

    yield "coroutine_level2"

def coroutine_level1():

    result = yield coroutine_level2()
    print("coroutine_level1: ", result)
    yield "coroutine_level1"

def nested_couroutines():

    result = yield coroutine_level1()
    print("nested_couroutines: ", result)
    yield

if __name__ == "__main__":
    
    sched = Scheduler()
    sched.new(nested_couroutines())
    # sched.new(syscall_couroutines())
    # multiple_couroutines(sched)
    sched.start()

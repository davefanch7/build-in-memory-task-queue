from asyncio import Queue, create_task
from dataclasses import dataclass, field
from typing import Any, Callable
import uuid

@dataclass
class Task:
    handler: Callable
    payload: Any
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

class TaskQueue:
    '''Initializes a queue with default concurrency of 3. List initialized for worker pool. '''
    def __init__(self, concurrency: int = 3):
        self.concurrency = concurrency
        self._queue = Queue()
        self._workers = []
        self._started = False

    def _ensure_started(self):
        if self._started:
            return
        self._workers = [create_task(self._worker(i)) for i in range(self.concurrency)]
        self._started = True

    async def _worker(self, worker_id: int):
        while True:
            task = await self._queue.get()
            try:
                await task.handler(task.payload)
            finally:
                self._queue.task_done()
    
    #adding tasks to the queue
    def enqueue(self, handler, payload):
        self._ensure_started()
        task = Task(handler=handler, payload=payload)
        self._queue.put_nowait(task)
        return task.id


        


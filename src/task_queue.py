from asyncio import Queue, create_task
from dataclasses import dataclass, field
from typing import Any, Callable
import uuid
import asyncio

@dataclass
class Task:
    handler: Callable
    payload: Any
    max_retries: int = 0
    backoff_ms: int = 1000
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
                await self._run_with_retries(task)
            finally:
                self._queue.task_done()
    
    async def _run_with_retries(self, task):
        attempt = 0
        while True:
            try:
                await task.handler(task.payload)
                return
            except Exception:
                if attempt>=task.max_retries:
                    raise
                backoff_seconds= (task.backoff_ms / 1000) * (2**attempt)
                await asyncio.sleep(backoff_seconds)
                attempt+=1

    async def _delayed_put(self, task, delay_ms):
        #run a delay before adding the task to the queue
        await asyncio.sleep(delay_ms/1000)
        self._queue.put_nowait(task)
    
    #adding tasks to the queue
    def enqueue(self, handler, payload, delay_ms=0, max_retries=0, backoff_ms=1000):
        self._ensure_started()
        task = Task(handler=handler, payload=payload, max_retries=max_retries, backoff_ms=backoff_ms)
        if delay_ms>0:
            asyncio.create_task(self._delayed_put(task, delay_ms))
        else:
            self._queue.put_nowait(task)
        return task.id


        


import pytest
import asyncio
from src.task_queue import TaskQueue

@pytest.mark.asyncio
async def test_enqueue():
    received=[]
    async def handler(payload):
        received.append(payload)

    queue=TaskQueue(concurrency=3)
    queue.enqueue(handler, {"to": "user@example.com", "body": "Hello"})

    await asyncio.sleep(0.05)

    assert received == [{"to": "user@example.com", "body": "Hello"}]
import asyncio
import logging 
from task_queue import TaskQueue

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

attempt_counts = {}

#------------handlers-----------------

async def send_email(payload):
    log.info(f'send_email running with payload: {payload}')


async def slow_task(payload):
    log.info(f"START task {payload['id']}")
    await asyncio.sleep(1)
    log.info(f"END task {payload['id']}")

async def flaky_handler(payload):
    task_id = payload["id"]
    attempt_counts[task_id] = attempt_counts.get(task_id, 0) + 1
    attempt = attempt_counts[task_id]

    if attempt < 3:
        log.info(f"[task {task_id}] attempt {attempt} FAILED")
        raise RuntimeError(f"simulated failure on attempt {attempt}")

    log.info(f"  [task {task_id}] attempt {attempt} SUCCEEDED")


async def always_fails_handler(payload):
    task_id = payload["id"]
    attempt_counts[task_id] = attempt_counts.get(task_id, 0) + 1
    attempt = attempt_counts[task_id]
    log.info(f"  [task {task_id}] attempt {attempt} FAILED")
    raise RuntimeError(f"permanent failure on attempt {attempt}")

#------------demos---------------------

async def demo_enqueue():
    log.info('Requirement 1: Enqueuing Tasks')
    log.info('Beginning demo..')
    queue=TaskQueue()
    task_id = queue.enqueue(send_email, {"to": "user@example.com", "body": "Hello"})
    log.info(f'Enqueued task with task_id: {task_id}')
    await asyncio.sleep(0.01)
    log.info('Done!')

async def demo_concurrency():
    log.info('Requirement 2: Concurrency')
    log.info('Beginning demo..')
    queue=TaskQueue(concurrency=2)
    for i in range(1,6):
        queue.enqueue(slow_task, {'id': i })
        log.info(f'Enqueued task {i}')
    await asyncio.sleep(3.5)


async def demo_delayed_execution():
    log.info("Requirement 3: Delayed Execution")
    log.info("Beginning demo..")
    queue = TaskQueue(concurrency=2)

    queue.enqueue(slow_task, {"id": "A"})
    log.info("enqueued task A (immediate, ~1s)")

    queue.enqueue(slow_task, {"id": "B"})
    log.info("enqueued task B (immediate, ~1s)")

    queue.enqueue(slow_task, {"id": "D"}, delay_ms=3000)
    log.info("enqueued task D (delayed 3s)")

    queue.enqueue(slow_task, {"id": "C"}, )
    log.info("enqueued task C (immediate, ~1s)")

    await asyncio.sleep(5)

async def demo_retries_with_backoff():
    log.info("Requirement 4: retry with exponential backoff")
    queue = TaskQueue(concurrency=3)

    log.info("enqueuing flaky task (will fail attempts 1, 2; succeed on 3)")
    log.info("max_retries=3, backoff_ms=1000 - expect sleeps of ~1s, ~2s")
    queue.enqueue(flaky_handler, {"id": "flaky-1"}, max_retries=3, backoff_ms=1000)

    await asyncio.sleep(3.5)

async def demo_dead_letter_queue():
    log.info("Requirement 5: DLQ")
    queue = TaskQueue(concurrency=3)

    log.info("enqueuing failing task with max_retries=2")
    queue.enqueue(always_fails_handler, {"id": "doomed-1"}, max_retries=2, backoff_ms=1000)

    await asyncio.sleep(3.5)

    log.info("Inspecting dead letter queue:")
    for entry in queue.get_dead_letters():
        log.info(f"task_id={entry.task_id[:8]} attempts={entry.attempts} error={entry.error}")


#-------entry point--------------

async def main():
    await demo_enqueue()
    log.info('')
    await demo_concurrency()
    log.info('')
    await demo_delayed_execution()
    log.info('')
    await demo_retries_with_backoff()
    log.info('')
    await demo_dead_letter_queue()

if __name__=='__main__':
    asyncio.run(main())
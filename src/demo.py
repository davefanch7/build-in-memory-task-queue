import asyncio
import logging 
from task_queue import TaskQueue

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

#------------handlers-----------------

async def send_email(payload):
    log.info(f'send_email running with payload: {payload}')


async def slow_task(payload):
    log.info(f"START task {payload['id']}")
    await asyncio.sleep(1)
    log.info(f"END task {payload['id']}")

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


#-------entry point--------------

async def main():
    await demo_enqueue()
    log.info('')
    await demo_concurrency()

if __name__=='__main__':
    asyncio.run(main())
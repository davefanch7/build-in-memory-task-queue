# Task: In-Memory Task Queue

> If you haven't read `README.md`, read it first. It explains how we want you to work, how `THINKING.md` fits in, and the no-AI rule. This file is just the problem.

## Context

You're building a backend service that processes jobs asynchronously: sending emails, resizing images, syncing data with a third-party API. You need a task queue that runs in-process. No Redis, no RabbitMQ, no SQS, just your application's own memory.

This is a library/module, not a CLI tool or web server. A caller imports it and uses it. Standard library only for the queue itself (test frameworks and dev tooling are fine).

Use whatever language you're strongest in. Python is a reasonable default if you have no preference.

## Requirements

Each requirement includes a code example showing the interface we expect. These are sketches of the **shape**, not exact signatures. Adapt to your language's idioms.

Implement all of the below in a single demo script with **timestamped console output** so that timing-dependent behaviour is visible from the logs. How you structure the output is up to you.

---

### 1. Enqueue tasks

Accept a handler function and a payload. The handler is async/callable, the payload is passed to it when the task runs.

```python
queue = TaskQueue(concurrency=3)

queue.enqueue(send_email, {"to": "user@example.com", "body": "Hello"})
```

---

### 2. Concurrency limit

At most N tasks running simultaneously. Configurable, default 3.

```python
queue = TaskQueue(concurrency=2)
```

To demonstrate: enqueue 5 tasks that each take ~1 second with `concurrency=2`. Your output should make it obvious that only 2 ever run at the same time.

---

### 3. Delayed execution

A task can be scheduled to run after a delay. A delayed task should not consume a concurrency slot while waiting.

```python
queue.enqueue(my_handler, my_payload, delay_ms=3000)
```

To demonstrate: enqueue a task with a 3-second delay. Your output should make it clear when the task was enqueued vs when it actually started running.

---

### 4. Retry with exponential backoff

Failed tasks retry up to a configurable number of times. Wait between attempts grows exponentially from a configurable base delay (e.g. base 1s gives waits of 1s, 2s, 4s). Both `max_retries` and `backoff_ms` are configurable per task.

```python
queue.enqueue(flaky_handler, payload, max_retries=3, backoff_ms=1000)
```

To demonstrate: enqueue a task that fails on attempts 1 and 2, then succeeds on attempt 3. Your output should show each failure, the wait between retries, and the eventual success.

---

### 5. Dead letter queue

Tasks that exhaust all retries go to a dead letter queue that can be inspected. Each entry should include enough for an operator to understand what failed: the task identifier, the error, and the number of attempts.

```python
dead_letters = queue.get_dead_letters()
```

To demonstrate: enqueue a task that always throws, configured with `max_retries=2`. Your output should show the 3 failed attempts (1 original + 2 retries) and the dead letter entry at the end.

---

### 6. Graceful shutdown

When `shutdown()` is called, the queue finishes in-progress tasks but doesn't start new ones. Callers should be able to await/block on shutdown completion. Tasks enqueued after shutdown is called should be rejected.

```python
await queue.shutdown()
```

To demonstrate: enqueue a slow task (~2 seconds), then immediately call `shutdown()`. Your output should show that shutdown waited for the in-progress task to finish before completing.

---

### 7. Concurrent enqueue safety

It should be safe to enqueue tasks from multiple threads / goroutines / async tasks at the same time. No crashes, no lost tasks.

To demonstrate: from multiple concurrent call sites, enqueue 20 tasks simultaneously. All 20 should complete without errors.

---

## Things to reason about

These are genuinely ambiguous design decisions with no single right answer. We'd like `THINKING.md` to engage with them as you go:

- How do you represent a task's lifecycle? Explicit state enum, or implicit from which collection it's in?
- What concurrency primitive do you use? Semaphore, worker pool, channels, something else? Why?
- Do retrying/delayed tasks hold a concurrency slot while they wait? Holding is simpler but wastes capacity. Releasing is efficient but needs a wake-up mechanism.
- What happens to tasks waiting for retry backoff when `shutdown()` is called?
- What's the synchronisation story for concurrent enqueue?
- How do you schedule "run after N ms"? A sleeping worker, a timer, a sorted queue?

If you make a call and later change your mind, write about that. Those moments are some of the best data we get.

---

## You're done when

- [ ] All seven requirements are implemented, or you've flagged in `THINKING.md` what you didn't get to and why.
- [ ] Your demo script runs and its output makes each scenario visibly correct.
- [ ] `THINKING.md` is filled in across all four sections, including the retrospective.
- [ ] The code runs from a clean clone with the setup instructions you provide.

Now open `THINKING.md` and write down your first reaction.

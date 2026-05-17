# Thinking Log

<!-- This is your scratchpad. Fill it in AS YOU GO, not at the end.
     Rough, fragmentary, honest. Don't polish it.
     Read the README for guidance on how to use this file. -->

## Initial Reaction

After reading the task initially, my first thought is that this is a challenging problem! The reason it's challenging is 2-fold - first, nowadays we have become very comfortable with using AI assistants to help us out, whethere it's helping research different topics or just building a start template. This will be refreshing to build without the help of AI though. The second challenge is that I have also been used to using existing queue services and have not had to build it ever from scratch. I have used both RabbitMQ in an on-prem setting and SQS for cloud development in AWS. That said, I am familiar with the concepts and have used them in applications/pipelines that I have built. 

As I read the task, one of my other thoughts was whether this needed to support both CPU bound and I/O bound handlers. Sending email & syncing data from a 3rd pary API are both IO, but resizing images could technically be CPU bound and doing calculations on pixels. The fact that async was mentioned multiple times though, I am going to make the assumption that this only needs to support IO bound handlers which means I can likely stick to threads and not worry about processes/cores. In the future though, that is something I would consider supporting as well. A user of this module could pass a "type" field where they specify whether they want either 'processes' or 'threads' to be used for their tasks. Anyway, off the top of my head I have used both the asyncio and multithreading Python libraries so I am aiming to use one of those, but will likely do research to see what my different options are and what might be best suited for the 7 tasks I need to handle. 

I also was thinking through the "queue" itself. I've used RabbitMQ and SQS, but never anything in-memory. I believe there is a collections module that could be used here, but again I will be doing some quick research to understand my different options and what might be best suited for the tasks I need to cover.

The tasks themselves seem to progress nicely in difficulty. The first few seem relatively straight forward. However, I am not entirely sure how I will handle delay / retries and deal with the concurrency piece. My initial thought on the delay was to use a time.sleep BEFORE adding it to the queue. That would make it easy to make sure a task does not get processed before a specified delay. However, the task says to queue the item first and then run the delay. At the moment, I am not entirely sure I will handle this! Might need more research here as well. 

One other thing that jumps out to me is that the 7 outlined objectives have clear, defined behavior. While the design choices are open (as far as the queue, processing, and code itself), the module has clear behaviors to support. This is sometimes the most difficult part of starting a new project - you know what the user / stakeholder is asking for, but the behaviors of your code are a bit more loose and you would want to spend more time upfront thinking through what your code/application needs to do. Here in this problem, we KNOW what we need to do, the question is how do we get there? This situation I prefer to take a test-driven development approach, so I'll try to write my test cases BEFORE writing my actual module. This can get tricky when it gets more into the retries, backoff, etc. But for now that's where my head is at.

Oh, and one other thing I wasn't sure on is if there are limits on the concurrency for in-memory. I know there has to be some sort of limit, but with threads I think it's pretty high? Anyway, my initial design I'm not going to worry about optimizing around concurrency or set any boundaries, as the task did not mention to do that. 


## Plan

<!-- Still before coding (or right at the start).
     - How will you structure this? Files, types, main components.
     - What are the key design decisions you're making up front?
     - What are you deliberately deferring?
     - What will you build FIRST — the smallest slice that proves something useful? -->

Start time - 2:10 pm 5/16

From my initial reaction, I knew I was going to ultimately go with either asyncio or multithreading as two built-in options. After a bit of research, I have decided to go with asyncio. I believe it has all of the features that I need to complete the 7 tasks, and will be a bit easier to implement than using the multithreading library.

I started by doing research into the asyncio library - I have only used this package here and there, so it was important for me to understand more, both conceptually and technically. Now, I feel a bit more comfortable with moving forward, but I know I will need to go back and forth with reference documents as I progress through the task. 


Initial plan for file structure is the following:
- src/task_queue.py -> this will be the module that I build. plan is to have a class TaskQueue() and then define different methods within there as needed
- tests/test_task_queue.py -> this will be for unit-testing my code. will be building out as I go
- src/demo.py -> this will be used for my own end-to-end testing and ultimately the final run that will validate if I have successfully built a module to meet the task specifications

I am deferring on deciding anything related to backoff/retries/delay/etc. I do not know how to implement these and to me it makes more sense to build my module piece-meal and research those more when I'm ready. 

To start, I am going to build the file structure, the initial Class, and then a method for enqueueing tasks, along with a unit test for that method. After I typed that, I realized testing async may be more challening than I thought - did quick research and there is pytest-asyncio so that should help me. 

## Progress Notes

<!-- Drop an entry any time you:
     - change direction from your plan
     - hit something unexpected
     - make a trade-off
     - realise you were wrong about something
     - finish a chunk and start the next

     One or two sentences each is fine. Timestamp each one.
     Imagine your pair partner just asked "what are you doing?" — answer that.
     Add as many entries as you need. -->

### [03:26 5/16]

I got my first successful test back for enqueueing tasks. My initial plan I did not realize I had to initialize a worker pool right away, quickly found that out when my enqueue method was not working. I also had to add __init__.py files in order for my pytests to operate correctly. 

### [12:05 5/17]

Starting to build out my demo.py script to demonstrate each task with timestamped logs. 

I built out the first demo then realized I need to reorganize demo.py to make it easy to demo each task. Each task will be a function
and I will start the queue within those functions to keep that task demo independent. I want each demo self-contained. 

I've now finished tasks 1 & 2. My class is successfully able to enqueue tasks and limit running tasks to a set concurrency.

### [HH:MM]

### [HH:MM]

### [HH:MM]

## Research / References

<!-- Optional. Any docs, articles, past code, or language references you looked at.
     A one-line note on what you took from each is enough. -->

AsyncIO documentation -> 
 https://realpython.com/async-io-python/?gad_source=1&gad_campaignid=23282418443&gbraid=0AAAAA_bFrtJyykW87ZXOIptUHNfSCyLlE&gclid=CjwKCAjwq6DQBhBVEiwA4ZD5XCprT6kiLGunKyVsuUnIY6pHTF1ubhwHr2tSuVQjGMQiT1YIORIQkBoC9csQAvD_BwE



## Retrospective

<!-- After you're done. This section is NOT optional — it's one of the most
     valuable parts of the submission. Be honest.

     - What's the weakest part of your solution? Where's the duct tape?
     - Where would this break in production?
     - What would you do differently with more time?
     - What surprised you about this problem?
     - Anything you tried and threw away? Why? -->

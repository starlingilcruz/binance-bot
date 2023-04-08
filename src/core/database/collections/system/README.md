# System Collections


## Resource

A resource is any class object that represents a memory space. 

We collect information about the class object creation, initialization, destruction, etc. 
to allow monitor the system activity and reach out any resource relation with any process.

Table definition: 

1. id
2. parent
3. type
4. status
5. created_at
6. updated_at
7. destroyed_at


## Operation

Represents any class object in memory that is related with an action, proccess or event.

Table definition:

1. id
2. parent
3. scope
4. resource_id
5. status
6. created_at
7. updated_at
8. destroyed_at

Operation States:

1. New: It is assigned to a process that is just created. It's the initial state of a process life cyle. 

2. Ready: The process is waiting to be assigned the processor by the short term scheduler, so it can run.
This state is immediately after the new state for the process.

3. Suspended: The process were initially in the ready state in main memory but lack of memory forced them to be suspended.

4. Running: The process is said to be in running state when the process instructions are being executed by the processor.

5. Blocked: The process is in blocked state if it is waiting for some event to occur. This event may be I/O as the I/O events are executed in the main memory and don't require the processor.

6. Terminanted: The process is terminated once it finishes its execution. In the terminated state, the process is removed from main memory and its process control block is also deleted.




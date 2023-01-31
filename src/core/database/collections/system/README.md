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


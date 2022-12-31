import asyncio
import inspect

import datetime
from time import sleep

# TODO move to utils
def is_coroutine(fn):
    return inspect.iscoroutinefunction(fn)

async def every(__seconds: float, func, *args, **kwargs):
    while True:
        if is_coroutine(func):
            await func(*args, **kwargs)
        else:
            func(*args, **kwargs)
        await asyncio.sleep(__seconds)

async def watch_ws_connectivity():
    # Ping the ws or check data is comming from ws
    pass

async def register_thread_trask(fn):
    # Register tasks that runs in separated thread
    pass

async def event_log(msg):
    print(msg)

async def init_runner(loop: asyncio.AbstractEventLoop, callbacks):
    asyncio.set_event_loop(loop)

    listeners = (
        watch_ws_connectivity(),
        # every(1, event_log, "Hello World"), # blocks current tread
        # every(1, print, "Hello World2") 
        every(5, callbacks)
    )

    for listener in listeners:
        await listener
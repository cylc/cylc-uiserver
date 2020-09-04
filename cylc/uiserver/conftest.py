import asyncio

import pytest


@pytest.fixture
def event_loop():
    """This fixture defines the event loop used for each test."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    # gracefully exit async generators
    loop.run_until_complete(loop.shutdown_asyncgens())
    # cancel any tasks still running in this event loop
    for task in asyncio.all_tasks(loop):
        task.cancel()
    loop.close()

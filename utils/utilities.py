import asyncio, sys

# Async console printing
async def aprint(string: str) -> None:
    await asyncio.to_thread(sys.stdout.write, f'{string}\n')

# Async parallel execution of Future objects
async def parallel_execute(coro_future_gens: list) -> None:
    await asyncio.gather(*coro_future_gens)
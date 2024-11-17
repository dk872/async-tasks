# The asynchronous map has been replaced with an asynchronous generator that processes elements one by one
import asyncio


async def async_generator_map(func, items, cancel_event):
    for item in items:
        if cancel_event.is_set():
            raise asyncio.CancelledError("Task was cancelled")
        try:
            yield await func(item)
        except Exception as e:
            yield f"Error: {e}"


async def operation_to_multiply(item):
    await asyncio.sleep(0.1)
    if not isinstance(item, (int, float)):
        raise TypeError(f"{type(item).__name__}")
    return item * 5


async def process_all_asynchronously(cancel_event):
    try:
        async for result in async_generator_map(operation_to_multiply, repeated_numbers_array, cancel_event):
            print(result)
    except asyncio.CancelledError:
        print("Processing was cancelled")


async def main():
    cancel_event = asyncio.Event()
    task = asyncio.create_task(process_all_asynchronously(cancel_event))

    await asyncio.sleep(5)
    cancel_event.set()
    await task


numbers_array = [1, 2, 'coconut', 4, 5, {'id': 4}]
repeated_numbers_array = numbers_array * 2000

asyncio.run(main())

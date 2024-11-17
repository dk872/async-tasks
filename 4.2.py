# The asynchronous generator processes elements in batches of one thousand
import asyncio


async def async_generator_map(func, items, cancel_event):
    for i in range(0, len(items), 1000):
        if cancel_event.is_set():
            raise asyncio.CancelledError("Task was cancelled")

        batch = items[i:i + 1000]
        try:
            yield await func(batch)
        except Exception as e:
            yield f"Error: {e}"


async def operation_to_multiply(batch):
    await asyncio.sleep(0.1)
    result = []
    for item in batch:
        if not isinstance(item, (int, float)):
            result.append(f"{type(item).__name__}")
        else:
            result.append(item * 5)
    return result


async def process_all_asynchronously(cancel_event):
    try:
        async for result in async_generator_map(operation_to_multiply, repeated_numbers_array, cancel_event):
            print(result)
    except asyncio.CancelledError:
        print("Processing was cancelled")


async def main():
    cancel_event = asyncio.Event()
    task = asyncio.create_task(process_all_asynchronously(cancel_event))

    await asyncio.sleep(1)
    cancel_event.set()
    await task


numbers_array = [1, 2, 'coconut', 4, 5, {'id': 4}]
repeated_numbers_array = numbers_array * 5000

asyncio.run(main())

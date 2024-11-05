# Implementation of asynchronous map using asyncio
import asyncio


async def async_map(func, items):
    tasks = [asyncio.create_task(func(item)) for item in items]
    results = []

    for task in tasks:
        try:
            result = await task
            results.append(result)
        except Exception as e:
            results.append(f"Error: {e}")

    return results


async def operation_to_multiply(item):
    await asyncio.sleep(1)
    if not isinstance(item, (int, float)):
        raise TypeError(f"{type(item).__name__}")
    return item * 5


async def operation_to_uppercase(item):
    await asyncio.sleep(1)
    if not isinstance(item, str):
        raise TypeError(f"{type(item).__name__}")
    return item.upper()


async def operation_process_object(item):
    await asyncio.sleep(1)
    if not isinstance(item, dict) or 'id' not in item:
        raise TypeError(f"{type(item).__name__}")
    return {**item, "processed": True}


numbers_array = [1, 2, 'coconut', 4, 5, {'id': 4}]
fruits_array = ['apple', 3, {'id': 5}, 'banana', 'mango']
objects_array = ['onion', {'id': 1}, {'id': 2}, {'id': 3}, 6]


async def process_all_asynchronously():
    tasks = [
        asyncio.create_task(async_map(operation_to_multiply, numbers_array)),
        asyncio.create_task(async_map(operation_to_uppercase, fruits_array)),
        asyncio.create_task(async_map(operation_process_object, objects_array))
    ]

    results = await asyncio.gather(*tasks)

    for result in results:
        print(result)


async def main():
    await process_all_asynchronously()


asyncio.run(main())

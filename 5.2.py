# An EventEmitter has also been added, but for processing elements in batches of one thousand
import asyncio


class EventEmitter:
    def __init__(self):
        self._listeners = {}

    def on(self, event, listener):
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(listener)

    def emit(self, event, *args):
        if event in self._listeners:
            for listener in self._listeners[event]:
                listener(*args)


async def async_generator_map(func, items, cancel_event, emitter):
    for i in range(0, len(items), 1000):
        if cancel_event.is_set():
            emitter.emit('task_cancelled')
            raise asyncio.CancelledError("Task was cancelled")

        batch = items[i:i + 1000]
        emitter.emit('batch_processed')

        try:
            yield await func(batch)
        except Exception as e:
            yield f"{e}"


async def operation_to_multiply(batch):
    await asyncio.sleep(0.1)
    result = []
    for item in batch:
        if not isinstance(item, (int, float)):
            result.append(f"{type(item).__name__}")
        else:
            result.append(item * 5)
    return result


async def process_all_asynchronously(cancel_event, emitter):
    try:
        async for result in async_generator_map(operation_to_multiply, repeated_numbers_array, cancel_event, emitter):
            print(result)
    except asyncio.CancelledError:
        print("Processing was cancelled")


def on_task_cancelled():
    print("The task was cancelled by the emitter")


def on_batch_processed():
    print("Processed batch:")


async def main():
    cancel_event = asyncio.Event()
    emitter = EventEmitter()

    emitter.on('task_cancelled', on_task_cancelled)
    emitter.on('batch_processed', on_batch_processed)

    task = asyncio.create_task(process_all_asynchronously(cancel_event, emitter))

    await asyncio.sleep(1)
    cancel_event.set()
    await task


numbers_array = [1, 2, 'coconut', 4, 5, {'id': 4}]
repeated_numbers_array = numbers_array * 5000

asyncio.run(main())

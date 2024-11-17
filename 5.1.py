# EventEmitter implementation has been added
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
    for item in items:
        if cancel_event.is_set():
            emitter.emit('task_cancelled')
            raise asyncio.CancelledError("Task was cancelled")
        try:
            yield await func(item)
        except Exception as e:
            emitter.emit('error_occurred', str(e))


async def operation_to_multiply(item):
    await asyncio.sleep(0.1)
    if not isinstance(item, (int, float)):
        raise TypeError(f"{type(item).__name__}")
    return item * 5


async def process_all_asynchronously(cancel_event, emitter):
    try:
        async for result in async_generator_map(operation_to_multiply, repeated_numbers_array, cancel_event, emitter):
            print(result)
    except asyncio.CancelledError:
        print("Processing was cancelled")


def on_task_cancelled():
    print("The task was cancelled by the emitter")


def on_error_occurred(error_message):
    print(f"An error occurred: {error_message}")


async def main():
    cancel_event = asyncio.Event()
    emitter = EventEmitter()

    emitter.on('task_cancelled', on_task_cancelled)
    emitter.on('error_occurred', on_error_occurred)

    task = asyncio.create_task(process_all_asynchronously(cancel_event, emitter))

    await asyncio.sleep(1)
    cancel_event.set()
    await task


numbers_array = [1, 2, 'coconut', 4, 5, {'id': 4}]
repeated_numbers_array = numbers_array * 2000

asyncio.run(main())

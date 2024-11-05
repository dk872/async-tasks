# Common use of map
def operation_to_multiply(item):
    return item * 5


def operation_to_uppercase(item):
    return item.upper()


def operation_process_object(item):
    return {**item, "processed": True}


numbers_array = [1, 2, 3, 4, 5]
fruits_array = ['apple', 'banana', 'mango']
objects_array = [{'id': 1}, {'id': 2}, {'id': 3}]


def process_all_synchronously():
    number_results = list(map(operation_to_multiply, numbers_array))
    print(number_results)

    fruit_results = list(map(operation_to_uppercase, fruits_array))
    print(fruit_results)

    object_results = list(map(operation_process_object, objects_array))
    print(object_results)


process_all_synchronously()

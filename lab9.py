# Лабораторная работа 9: Жадные алгоритмы
import heapq

# Задача A: Выбор максимального количества активностей

def max_activities(activities):
    """
    Жадная стратегия:
    Сортируем активности по времени их окончания.
    Берем самую раннюю закончившуюся активность, чтобы оставить
    как можно больше свободного времени для следующих.
    """
    if not activities:
        return []

    # Сортировка по времени завершения (второй элемент кортежа)
    sorted_activities = sorted(activities, key=lambda x: x[1])

    selected = [sorted_activities[0]]
    last_end_time = sorted_activities[0][1]

    for start, end in sorted_activities[1:]:
        # Если активность начинается не раньше, чем закончилась предыдущая
        if start >= last_end_time:
            selected.append((start, end))
            last_end_time = end

    return selected



# Задача B: Непрерывный (дробный) рюкзак

def fractional_knapsack(items, capacity):
    """
    Жадная стратегия:
    Сортируем предметы по удельной стоимости (стоимость / вес) по убыванию.
    Берем максимально дорогие за единицу веса предметы.
    """
    # стоимость/вес
    items_with_ratio = []
    for val, weight in items:
        ratio = val / weight
        items_with_ratio.append((ratio, val, weight))


    items_with_ratio.sort(key=lambda x: x[0], reverse=True)

    total_value = 0.0
    remaining_capacity = capacity
    taken_items = []

    for ratio, val, weight in items_with_ratio:
        if remaining_capacity <= 0:
            break

        if weight <= remaining_capacity:
            #  предмет целиком
            remaining_capacity -= weight
            total_value += val
            taken_items.append((val, weight, 1.0))  # 1.0 = 100%
        else:
            # долю предмета
            fraction = remaining_capacity / weight
            total_value += val * fraction
            taken_items.append((val, weight, round(fraction, 2)))
            remaining_capacity = 0

    return total_value, taken_items



# Задача C: Минимизация стоимости соединения кабелей

def min_cable_merge_cost(cables):
    """
    Жадная стратегия:
    На каждом шаге всегда соединяем два САМЫХ КОРОТКИХ куска кабеля.
    Для эффективного поиска минимумов используется структура данных Min-Heap (куча).
    """
    if not cables or len(cables) <= 1:
        return 0


    heap = cables.copy()
    heapq.heapify(heap)

    total_cost = 0

    # Пока не объединим все куски в один
    while len(heap) > 1:
        first = heapq.heappop(heap)
        second = heapq.heappop(heap)

        merge_cost = first + second
        total_cost += merge_cost


        heapq.heappush(heap, merge_cost)

    return total_cost



if __name__ == "__main__":
    print("--- Задача A: Выбор активностей ---")
    activities_input = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 8), (5, 9),
                        (6, 10), (8, 11), (8, 12), (2, 13), (12, 14)]
    chosen_activities = max_activities(activities_input)
    print(f"Исходные активности: {activities_input}")
    print(f"Выбранные активности ({len(chosen_activities)} шт.): {chosen_activities}\n")

    print("--- Задача B: Дробный рюкзак ---")
    items_input = [(60, 10), (100, 20), (120, 30)]  # (стоимость, вес)
    knapsack_capacity = 50
    max_val, items_taken = fractional_knapsack(items_input, knapsack_capacity)
    print(f"Предметы (стоимость, вес): {items_input}")
    print(f"Вместимость рюкзака: {knapsack_capacity}")
    print(f"Максимальная стоимость: {max_val}")
    print(f"Взятые предметы (стоимость, вес, доля): {items_taken}\n")

    print("--- Задача C: Соединение кабелей ---")
    cables_input = [4, 3, 2, 6]
    total_merge_cost = min_cable_merge_cost(cables_input)
    print(f"Длины кабелей: {cables_input}")
    print(f"Минимальная общая стоимость соединений: {total_merge_cost}")
# пример №1

def max_subarray_sum(numbers):
    dp = [0] * len(numbers)
    dp[0] = numbers[0]

    for i in range(1, len(numbers)):
        dp[i] = max(numbers[i], dp[i - 1] + numbers[i])

    return max(dp)


tests = [
    ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
    ([1, 2, 3, 4], 10),
    ([-5, -2, -8], -2),
    ([7], 7),
    ([0, -1, 0], 0)
]

passed = 0

for number, (numbers, expected) in enumerate(tests, 1):
    result = max_subarray_sum(numbers)
    status = "Пройден" if result == expected else "Ошибка"
    passed += result == expected

    print(f"Тест {number}: {numbers}")
    print(f"Результат: {result}, ожидалось: {expected}")
    print(f"Статус: {status}\n")

print(f"Пройдено тестов: {passed} из {len(tests)}")


# Пример №2

def lis_length(numbers):
    if not numbers:
        return 0

    dp = [1] * len(numbers)

    for i in range(len(numbers)):
        for j in range(i):
            if numbers[j] < numbers[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


tests = [
    ([3, 1, 2, 5, 4], 3),
    ([1, 2, 3, 4, 5], 5),
    ([5, 4, 3, 2, 1], 1),
    ([2, 2, 2], 1),
    ([], 0)
]

passed = 0

for number, (numbers, expected) in enumerate(tests, 1):
    result = lis_length(numbers)
    status = "Пройден" if result == expected else "Ошибка"
    passed += result == expected

    print(f"Тест {number}: {numbers}")
    print(f"Результат: {result}, ожидалось: {expected}")
    print(f"Статус: {status}\n")

print(f"Пройдено тестов: {passed} из {len(tests)}")


# Пример №3

def lcs_length(first, second):
    n = len(first)
    m = len(second)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if first[i - 1] == second[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[n][m]


tests = [
    ("abcde", "ace", 3),
    ("abc", "abc", 3),
    ("abc", "def", 0),
    ("", "abc", 0),
    ("aaaa", "aa", 2)
]

passed = 0

for number, (first, second, expected) in enumerate(tests, 1):
    result = lcs_length(first, second)
    status = "Пройден" if result == expected else "Ошибка"
    passed += result == expected

    print(f"Тест {number}: '{first}' и '{second}'")
    print(f"Результат: {result}, ожидалось: {expected}")
    print(f"Статус: {status}\n")

print(f"Пройдено тестов: {passed} из {len(tests)}")


# Пример №3


def lcs_length(first, second):
    n = len(first)
    m = len(second)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if first[i - 1] == second[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[n][m]


tests = [
    ("abcde", "ace", 4),
    ("abc", "abc", 3),
    ("abc", "def", 0),
    ("", "abc", 0),
    ("aaaa", "aa", 2)
]

passed = 0

for number, (first, second, expected) in enumerate(tests, 1):
    result = lcs_length(first, second)
    status = "Пройден" if result == expected else "Ошибка"
    passed += result == expected

    print(f"Тест {number}: '{first}' и '{second}'")
    print(f"Результат: {result}, ожидалось: {expected}")
    print(f"Статус: {status}\n")

print(f"Пройдено тестов: {passed} из {len(tests)}")
import random
import statistics
import matplotlib.pyplot as plt
import cProfile
import pstats
import io


def generate_random_numbers(n, lower_bound=0, upper_bound=100):
    """Генерация списка случайных чисел."""
    return [random.randint(lower_bound, upper_bound) for _ in range(n)]


def square_numbers(numbers):
    """Возвращает списки квадратов чисел."""
    return [x ** 2 for x in numbers]


def filter_even_numbers(numbers):
    """Фильтрует четные числа из списка."""
    return [x for x in numbers if x % 2 == 0]


def calculate_average(numbers):
    """Вычисляет среднее значение списка чисел."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


def calculate_median(numbers):
    """Вычисляет медиану списка чисел."""
    if not numbers:
        return 0
    return statistics.median(numbers)


def plot_histogram(numbers):
    """Строит гистограмму для чисел."""
    plt.hist(numbers, bins=10, edgecolor='black')
    plt.title('Гистограмма четных квадратов')
    plt.xlabel('Значения')
    plt.ylabel('Частота')
    plt.show()


def save_to_file(numbers, filename='output.txt'):
    """Сохраняет список чисел в файл."""
    with open(filename, 'w') as file:
        for number in numbers:
            file.write(f"{number}\n")
    print(f"Результаты сохранены в {filename}")


def main():
    choice = input("Хотите сгенерировать случайные числа (введите 'y') или ввести их вручную (введите 'n')? ")

    if choice.lower() == 'y':
        num_count = 50
        random_numbers = generate_random_numbers(num_count)
    else:
        numbers_input = input("Введите числа через запятую: ")
        random_numbers = list(map(int, numbers_input.split(',')))

    print("Сгенерированные/введенные числа:")
    print(random_numbers)

    squared_numbers = square_numbers(random_numbers)

    print("\nКвадраты введенных чисел:")
    print(squared_numbers)

    even_numbers = filter_even_numbers(squared_numbers)

    print("\nЧетные числа из квадратов:")
    print(even_numbers)

    average = calculate_average(even_numbers)
    median = calculate_median(even_numbers)

    print("\nСреднее значение четных квадратов:", average)
    print("Медиана четных квадратов:", median)

    sorted_even_numbers = sorted(even_numbers)
    print("\nОтсортированные четные квадраты:")
    print(sorted_even_numbers)

    if even_numbers:
        max_even = max(even_numbers)
        min_even = min(even_numbers)
        print("\nМаксимальное четное число из квадратов:", max_even)
        print("Минимальное четное число из квадратов:", min_even)
    else:
        print("Нет четных квадратов.")

    if even_numbers:
        print("\nЕсть четные квадраты.")
    else:
        print("\nЧетных квадратов нет.")

    frequency = {}
    for num in sorted_even_numbers:
        frequency[num] = frequency.get(num, 0) + 1

    print("\nЧастота четных квадратов:")
    for number, count in frequency.items():
        print(f"Число {number} встречается {count} раз.")

    plot_histogram(even_numbers)

    save_to_file(sorted_even_numbers)

    print("\nЗавершение программы.")


def profile():
    pr = cProfile.Profile()
    pr.enable()

    main()

    pr.disable()
    s = io.StringIO()
    sortby = pstats.SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    with open("profiler_output.txt", "w") as f:
        f.write(s.getvalue())


if __name__ == "__main__":
    profile()

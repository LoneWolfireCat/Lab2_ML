import numpy as np
import matplotlib.pyplot as plt


# Функция для определения трапециевидной функции принадлежности
def trapezoidal_mf(x, a, b, c, d):
    """
    Трапециевидная функция принадлежности.
    :param x: Точки, для которых вычисляется функция принадлежности.
    :param a: Левая граница начала возрастания функции.
    :param b: Левая верхняя граница (где функция равна 1).
    :param c: Правая верхняя граница (где функция равна 1).
    :param d: Правая граница окончания убывания функции.
    :return: Значение функции принадлежности в точках x.
    """
    result = np.zeros_like(x)

    # Условия для трапециевидной функции
    condition1 = (x >= a) & (x < b)
    condition2 = (x >= b) & (x <= c)
    condition3 = (x > c) & (x <= d)

    # Вычисляем значения для каждой части
    result[condition1] = (x[condition1] - a) / (b - a) if b != a else 1.0
    result[condition2] = 1.0
    result[condition3] = (d - x[condition3]) / (d - c) if d != c else 1.0

    return result


# Операция пересечения нечетких множеств (минимум)
def fuzzy_intersection(set1, set2):
    return np.minimum(set1, set2)


# Универсум для активности пользователей (посты в день)
x_activity = np.linspace(0, 20, 500)

# Универсум для вовлеченности (лайки, комментарии, репосты в день)
x_engagement = np.linspace(0, 50, 500)

# Определение трапециевидных функций для активности пользователей
# Исправленные параметры для лучшего покрытия
low_activity = trapezoidal_mf(x_activity, 0, 0, 3, 6)
medium_activity = trapezoidal_mf(x_activity, 2, 5, 8, 12)
high_activity = trapezoidal_mf(x_activity, 8, 12, 20, 20)

# Определение трапециевидных функций для вовлеченности
# Исправленные параметры для лучшего покрытия
inactive = trapezoidal_mf(x_engagement, 0, 0, 8, 15)
low_engagement = trapezoidal_mf(x_engagement, 5, 12, 18, 25)
active = trapezoidal_mf(x_engagement, 15, 22, 28, 35)
highly_active = trapezoidal_mf(x_engagement, 25, 32, 50, 50)

# Ввод данных от пользователя
print("=== Анализ социальных сетей ===")
print("Введите параметры для анализа:")

try:
    # Активность пользователя
    activity_value = float(input("Количество постов в день (0-20): "))
    engagement_value = float(input("Количество взаимодействий в день (0-50): "))

    # Проверка на выход за границы универсума
    if activity_value < 0 or activity_value > 20:
        print("Ошибка: активность должна быть в диапазоне 0-20")
        exit()
    if engagement_value < 0 or engagement_value > 50:
        print("Ошибка: вовлеченность должна быть в диапазоне 0-50")
        exit()

except ValueError:
    print("Ошибка: введите числовые значения")
    exit()


# Функция для вычисления принадлежности для конкретного значения
def calculate_membership(value, x_universe, mf):
    # Находим ближайший индекс в универсуме
    idx = np.argmin(np.abs(x_universe - value))
    return mf[idx]


# Вычисление степени принадлежности для активности
activity_membership = [
    calculate_membership(activity_value, x_activity, low_activity),
    calculate_membership(activity_value, x_activity, medium_activity),
    calculate_membership(activity_value, x_activity, high_activity)
]

# Вычисление степени принадлежности для вовлеченности
engagement_membership = [
    calculate_membership(engagement_value, x_engagement, inactive),
    calculate_membership(engagement_value, x_engagement, low_engagement),
    calculate_membership(engagement_value, x_engagement, active),
    calculate_membership(engagement_value, x_engagement, highly_active)
]

# Вывод результатов принадлежности
print("\n=== Степень принадлежности ===")
print(f"Активность {activity_value} постов/день:")
print(f"  Низкая: {activity_membership[0]:.3f}")
print(f"  Средняя: {activity_membership[1]:.3f}")
print(f"  Высокая: {activity_membership[2]:.3f}")

print(f"\nВовлеченность {engagement_value} взаимодействий/день:")
print(f"  Неактивный: {engagement_membership[0]:.3f}")
print(f"  Малоактивный: {engagement_membership[1]:.3f}")
print(f"  Активный: {engagement_membership[2]:.3f}")
print(f"  Сильно активный: {engagement_membership[3]:.3f}")
# Визуализация результатов
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# График 1: Функции принадлежности для активности
ax1.plot(x_activity, low_activity, 'b-', label='Низкая активность', linewidth=2)
ax1.plot(x_activity, medium_activity, 'g-', label='Средняя активность', linewidth=2)
ax1.plot(x_activity, high_activity, 'r-', label='Высокая активность', linewidth=2)
ax1.axvline(x=activity_value, color='k', linestyle='--', label=f'Текущая активность: {activity_value}')
ax1.set_title('Нечеткие множества для активности пользователей')
ax1.set_xlabel('Количество постов в день')
ax1.set_ylabel('Степень принадлежности')
ax1.legend()
ax1.grid(True)

# График 2: Функции принадлежности для вовлеченности
ax2.plot(x_engagement, inactive, 'b-', label='Неактивный', linewidth=2)
ax2.plot(x_engagement, low_engagement, 'c-', label='Малоактивный', linewidth=2)
ax2.plot(x_engagement, active, 'g-', label='Активный', linewidth=2)
ax2.plot(x_engagement, highly_active, 'r-', label='Сильно активный', linewidth=2)
ax2.axvline(x=engagement_value, color='k', linestyle='--', label=f'Текущая вовлеченность: {engagement_value}')
ax2.set_title('Нечеткие множества для вовлеченности пользователей')
ax2.set_xlabel('Количество взаимодействий в день')
ax2.set_ylabel('Степень принадлежности')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()

# Вывод результатов пересечения для текущих значений
print("\n=== Результаты пересечения для текущих значений ===")
current_intersections = []

activity_labels = ["Низкая", "Средняя", "Высокая"]
engagement_labels = ["Неактивная", "Малоактивная", "Активная", "Сильно активная"]

for i, activity_mf in enumerate(activity_membership):
    for j, engagement_mf in enumerate(engagement_membership):
        intersection_value = min(activity_mf, engagement_mf)
        current_intersections.append((intersection_value, i, j))

# Сортировка по убыванию степени принадлежности
current_intersections.sort(reverse=True, key=lambda x: x[0])

print("Наиболее вероятные комбинации:")
found_valid = False
for i, (value, act_idx, eng_idx) in enumerate(current_intersections):
    if value > 0.01:  # Небольшой порог для учета числовых погрешностей
        print(f"{i+1}. {activity_labels[act_idx]} активность ∩ {engagement_labels[eng_idx]} вовлеченность: {value:.3f}")
        found_valid = True

if not found_valid:
    print("Нет значимых пересечений. Попробуйте другие значения.")
    print("Рекомендуемые тестовые значения:")
    print("  Активность: 2, 6, 10 постов/день")
    print("  Вовлеченность: 10, 20, 30 взаимодействий/день")
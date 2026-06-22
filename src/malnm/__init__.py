# malnm/__init__.py

from .methods import METHODS, SECTIONS
import difflib

__version__ = "3.5.0"


# --------------------- БАЗОВЫЕ ФУНКЦИИ ДЛЯ МЕТОДОВ ---------------------

def _get_method(method_name, output_type):
    """Возвращает запрошенную информацию по методу."""
    if method_name not in METHODS:
        raise ValueError(f"Метод '{method_name}' не найден. Используйте malnm.help()")
    data = METHODS[method_name]
    if output_type == 't':
        return data['theory']
    elif output_type == 'c':
        return data['code']
    elif output_type == 'v':
        return data['visualization']
    else:
        raise ValueError("output_type должен быть 't', 'c' или 'v'")


def _create_function(method_name):
    """Создает функцию для метода."""

    def func(output_type):
        return _get_method(method_name, output_type)

    func.__name__ = method_name
    func.__doc__ = f"Вывод шпаргалки по методу {METHODS[method_name]['full_name']}. Аргумент: 't' - теория, 'c' - код, 'v' - визуализация."
    return func


# Динамически создаём функции в текущем модуле
for name in METHODS:
    globals()[name] = _create_function(name)


# --------------------- ФУНКЦИЯ HELP ---------------------

def help():
    """Выводит список всех доступных методов."""
    print("Доступные методы:")
    print("=" * 80)
    for i, (name, data) in enumerate(METHODS.items(), 1):
        aliases = f" ({', '.join(data['aliases'])})" if data['aliases'] else ""
        section_info = f"[Раздел {data['section']}: {SECTIONS[data['section']]}]"
        print(f"{i:2d}. {data['full_name']}{aliases}")
        print(f"    Функция: {name}")
        print(f"    {section_info}")
        print()
    print("=" * 80)
    print("Использование:")
    print("  malnm.<функция>('t')  - теория")
    print("  malnm.<функция>('c')  - код")
    print("  malnm.<функция>('v')  - визуализация")
    print("  malnm.question('текст') - поиск вопроса и ответа")
    print("  malnm.topic('тема')   - поиск теории по теме")
    print("  malnm.topic('all')    - список всех тем")


# --------------------- ФУНКЦИЯ QUESTION ---------------------

def question(query):
    """
    Поиск вопроса и ответа по ключевому слову или фразе.
    query - строка для поиска (регистронезависимый частичный поиск).
    """
    found = []
    query_lower = query.lower()
    for method_name, data in METHODS.items():
        for item in data.get('qa', []):
            q, a = item['question'], item['answer']
            if query_lower in q.lower() or query_lower in a.lower():
                found.append((method_name, q, a))
    if found:
        print(f"Найдено {len(found)} совпадений:")
        for method, q, a in found:
            print(f"\nМетод: {method}")
            print(f"Вопрос: {q}")
            print(f"Ответ: {a}")
    else:
        # Поиск в теории
        for method_name, data in METHODS.items():
            theory = data.get('theory', '')
            if query_lower in theory.lower():
                lines = theory.split('\n')
                for i, line in enumerate(lines):
                    if query_lower in line.lower():
                        start = max(0, i - 2)
                        end = min(len(lines), i + 3)
                        print(f"\nМетод: {method_name}")
                        print('\n'.join(lines[start:end]))
                        return
        print("Ничего не найдено. Попробуйте изменить запрос.")


# --------------------- ФУНКЦИЯ TOPIC ---------------------

# Словарь тем с ключевыми словами и связанными методами
TOPICS = {
    'погрешность': {
        'keywords': ['погрешность', 'ошибка', 'точность', 'абсолютная', 'относительная', 'верные цифры',
                     'значащие цифры', 'округление'],
        'methods': ['bisection', 'newton', 'modified_newton', 'secant', 'fixed_point', 'floating_point', 'kahan_sum'],
        'description': 'Погрешности вычислений: абсолютная и относительная, верные цифры, округление, потеря значимости.'
    },
    'сходимость': {
        'keywords': ['сходимость', 'скорость сходимости', 'линейная', 'квадратичная', 'сверхлинейная', 'порядок'],
        'methods': ['bisection', 'newton', 'modified_newton', 'secant', 'fixed_point', 'fixed_point_system',
                    'newton_2d', 'modified_newton_2d', 'gauss_seidel', 'power_method', 'power_method_shift',
                    'qr_algorithm', 'jacobi_eigen'],
        'description': 'Скорость и условия сходимости итерационных методов.'
    },
    'устойчивость': {
        'keywords': ['устойчивость', 'стабильность', 'строгая', 'слабая', 'условная', 'безусловная',
                     'распространение ошибки'],
        'methods': ['newton', 'euler', 'predictor_corrector', 'rk4', 'adams_bashforth_2', 'adams_moulton_2',
                    'floating_point'],
        'description': 'Устойчивость численных методов, строгая и слабая устойчивость.'
    },
    'интерполяция': {
        'keywords': ['интерполяция', 'экстраполяция', 'аппроксимация', 'глобальная', 'локальная', 'сплайн', 'Лагранж',
                     'линейная', 'кубическая'],
        'methods': ['lagrange', 'linear_interp', 'cubic_spline'],
        'description': 'Интерполяция: глобальная и локальная, линейная, Лагранжа, кубические сплайны.'
    },
    'матрицы': {
        'keywords': ['матрица', 'умножение', 'плотная', 'разреженная', 'хранение', 'CSR', 'CSC', 'COO'],
        'methods': ['matmul_naive', 'strassen', 'gauss_seidel', 'qr_gram_schmidt', 'qr_algorithm', 'jacobi_eigen',
                    'schur_decomposition', 'svd', 'pca'],
        'description': 'Матричные операции, плотные и разреженные матрицы, способы хранения.'
    },
    'собственные значения': {
        'keywords': ['собственное значение', 'собственный вектор', 'спектральный радиус', 'отношение Релея',
                     'круги Гершгорина', 'характеристический многочлен'],
        'methods': ['power_method', 'power_method_shift', 'qr_algorithm', 'jacobi_eigen', 'schur_decomposition',
                    'eigen_values_2x2'],
        'description': 'Собственные значения и векторы, методы их нахождения.'
    },
    'ОДУ': {
        'keywords': ['ОДУ', 'дифференциальное уравнение', 'Эйлер', 'Рунге-Кутта', 'Адамс', 'многошаговый', 'явный',
                     'неявный', 'предиктор-корректор'],
        'methods': ['euler', 'predictor_corrector', 'rk4', 'adams_bashforth_2', 'adams_moulton_2',
                    'numerical_derivative'],
        'description': 'Обыкновенные дифференциальные уравнения, явные и неявные методы.'
    },
    'Фурье': {
        'keywords': ['Фурье', 'ДПФ', 'БПФ', 'спектр', 'амплитудный', 'частотный', 'фильтрация', 'сезонность',
                     'дискретизация'],
        'methods': ['dft', 'fft'],
        'description': 'Дискретное преобразование Фурье, спектральный анализ, фильтрация сигналов.'
    },
    'IEEE 754': {
        'keywords': ['IEEE 754', 'плавающая точка', 'float', 'double', 'машинный эпсилон', 'NaN', 'Inf', 'underflow',
                     'overflow'],
        'methods': ['floating_point', 'kahan_sum', 'matmul_naive', 'lagrange'],
        'description': 'Представление чисел с плавающей точкой, стандарт IEEE 754, ошибки округления.'
    },
    'профилирование': {
        'keywords': ['профилирование', 'профайлинг', 'cProfile', 'timeit', 'сложность', 'big-O', 'производительность',
                     'оптимизация'],
        'methods': ['profiling'],
        'description': 'Профилирование кода, измерение производительности, сложность алгоритмов.'
    }
}


def topic(topic_name):
    """
    Поиск теории по теме.
    topic_name - название темы или ключевое слово.
    malnm.topic('all') - выводит список всех доступных тем.
    """
    # Если запрошен список всех тем
    if topic_name.lower() == 'all':
        print("Доступные темы:")
        print("=" * 80)
        for name, data in TOPICS.items():
            print(f"\n{name.upper()}:")
            print(f"  {data['description']}")
            print(f"  Связанные методы: {', '.join(data['methods'])}")
            print(f"  Ключевые слова: {', '.join(data['keywords'])}")
        print("\n" + "=" * 80)
        print("Использование: malnm.topic('название_темы')")
        return

    # Поиск по ключевым словам
    topic_lower = topic_name.lower()
    found_topics = []

    for name, data in TOPICS.items():
        # Проверяем по названию темы
        if topic_lower in name.lower():
            found_topics.append((name, data))
            continue
        # Проверяем по ключевым словам
        for keyword in data['keywords']:
            if topic_lower in keyword.lower():
                found_topics.append((name, data))
                break

    if not found_topics:
        print(f"Тема '{topic_name}' не найдена. Используйте malnm.topic('all') для списка всех тем.")
        return

    for name, data in found_topics:
        print(f"\n{'=' * 80}")
        print(f"ТЕМА: {name.upper()}")
        print(f"{'=' * 80}")
        print(f"\n{data['description']}")
        print(f"\nСвязанные методы: {', '.join(data['methods'])}")
        print(f"\nКлючевые слова: {', '.join(data['keywords'])}")

        # Собираем теорию из связанных методов
        print("\n" + "-" * 40)
        print("ТЕОРИЯ ПО ТЕМЕ:")
        print("-" * 40)

        theory_parts = []
        for method_name in data['methods']:
            if method_name in METHODS:
                method_data = METHODS[method_name]
                theory = method_data.get('theory', '')
                if theory:
                    # Извлекаем релевантные части теории (ищем по ключевым словам)
                    lines = theory.split('\n')
                    relevant_lines = []
                    for i, line in enumerate(lines):
                        line_lower = line.lower()
                        for keyword in data['keywords']:
                            if keyword.lower() in line_lower:
                                # Берём контекст: 2 строки до и 2 после
                                start = max(0, i - 2)
                                end = min(len(lines), i + 3)
                                context = lines[start:end]
                                if context not in relevant_lines:
                                    relevant_lines.extend([''] + context)
                                break
                    if relevant_lines:
                        theory_parts.append(f"\n[Из метода {method_name}]:")
                        theory_parts.extend(relevant_lines)

        if theory_parts:
            print('\n'.join(theory_parts))
        else:
            print("(Теория по данной теме встроена в описания методов)")

        # Выводим Q&A из связанных методов
        print("\n" + "-" * 40)
        print("ВОПРОСЫ И ОТВЕТЫ ПО ТЕМЕ:")
        print("-" * 40)

        qa_found = False
        for method_name in data['methods']:
            if method_name in METHODS:
                qa_list = METHODS[method_name].get('qa', [])
                for item in qa_list:
                    q = item['question']
                    a = item['answer']
                    # Проверяем, относится ли вопрос к теме
                    q_lower = q.lower()
                    for keyword in data['keywords']:
                        if keyword.lower() in q_lower:
                            print(f"\n[{method_name}]\nВ: {q}\nО: {a}")
                            qa_found = True
                            break

        if not qa_found:
            print("(Специализированные вопросы по теме находятся в описаниях методов)")


# --------------------- ИНИЦИАЛИЗАЦИЯ ---------------------

# Добавляем информацию о новых методах в SECTIONS
SECTIONS[4] = "Общая теория вычислений (IEEE 754, погрешности, устойчивость)"
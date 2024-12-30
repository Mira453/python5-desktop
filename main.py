from itertools import product

# Функція для побудови таблиці істинності
def build_truth_table():
    variables = ['x', 'y', 'z']
    table = list(product([0, 1], repeat=3))
    return table

# Функція для обчислення значення функції для кожної комбінації змінних
def calculate_function_values(table, f_values):
    result = []
    for row, value in zip(table, f_values):
        result.append((*row, value))
    return result

# Функція для знаходження ДДНФ
def find_ddnf(table, f_values):
    terms = []
    for row, f in zip(table, f_values):
        if f == 1:
            term = "".join(f"{var}" if bit else f"{var}'" for var, bit in zip(['x', 'y', 'z'], row))
            terms.append(term)
    return " + ".join(terms)

# Функція для знаходження ДКНФ
def find_dknf(table, f_values):
    terms = []
    for row, f in zip(table, f_values):
        if f == 0:
            term = "(" + " + ".join(f"{var}'" if bit else f"{var}" for var, bit in zip(['x', 'y', 'z'], row)) + ")"
            terms.append(term)
    return " * ".join(terms)

# Функція для представлення поліномом Жегалкіна
def zhegalkin_polynomial(f_values):
    n = len(f_values)
    coefficients = f_values[:]
    for i in range(n):
        for j in range(n - i - 1):
            coefficients[j] ^= coefficients[j + 1]
    terms = []
    for idx, coef in enumerate(coefficients):
        if coef == 1:
            bin_idx = f"{idx:03b}"
            term = "".join([var for var, bit in zip(['x', 'y', 'z'], map(int, bin_idx)) if bit])
            terms.append(term if term else "1")
    return " ⊕ ".join(terms)

# Функція для перевірки властивостей функції
def check_properties(f_values):
    properties = {
        "Зберігає константу 0": f_values[0] == 0,
        "Зберігає константу 1": f_values[-1] == 1,
        "Самодвоїстість": all(f_values[i] != f_values[-i-1] for i in range(len(f_values) // 2)),
        "Монотонність": all(f_values[i] <= f_values[j] for i in range(len(f_values)) for j in range(i+1, len(f_values)) if all(x <= y for x, y in zip(f"{i:03b}", f"{j:03b}"))),
        "Лінійність": all(sum(int(a) & int(b) for a, b in zip(f"{x:03b}", f"{y:03b}")) % 2 == 0 or (f_values[x] ^ f_values[y]) == f_values[x ^ y] for x in range(8) for y in range(x, 8))
    }
    return properties

# Основна частина програми
if __name__ == "__main__":
    # Значення функції (F = 00100100)
    f_values = [0, 0, 1, 0, 0, 1, 0, 0]
    
    # Побудова таблиці істинності
    table = build_truth_table()
    
    # Обчислення значень функції для таблиці істинності
    truth_table = calculate_function_values(table, f_values)
    print("Таблиця істинності:")
    for row in truth_table:
        print(row)
    
    # Пошук ДДНФ
    ddnf = find_ddnf(table, f_values)
    print("\nДДНФ:", ddnf)
    
    # Пошук ДКНФ
    dknf = find_dknf(table, f_values)
    print("\nДКНФ:", dknf)
    
    # Поліном Жегалкіна
    zhegalkin = zhegalkin_polynomial(f_values)
    print("\nПоліном Жегалкіна:", zhegalkin)
    
    # Перевірка властивостей
    properties = check_properties(f_values)
    print("\nВластивості функції:")
    for prop, value in properties.items():
        print(f"{prop}: {'Так' if value else 'Ні'}")

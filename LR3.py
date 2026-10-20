import math
import os
import heapq
from collections import Counter

# --- Вспомогательные функции ---

def get_entropy(probabilities):
    """Вычисляет энтропию по списку вероятностей."""
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def calculate_average_length(codes, probabilities_dict):
    """Вычисляет среднюю длину кодового слова."""
    return sum(len(codes[char]) * prob for char, prob in probabilities_dict.items())

# --- Построение кодов ---

def build_uniform_code(alphabet):
    """Строит равномерный код."""
    n = len(alphabet)
    bits = math.ceil(math.log2(n))
    codes = {}
    for i, char in enumerate(alphabet):
        codes[char] = format(i, f'0{bits}b')
    return codes

def build_shannon_fano_code(frequencies):
    """Строит код Шеннона-Фано (рекурсивно)."""
    # Сортируем символы по убыванию частоты
    sorted_chars = sorted(frequencies.keys(), key=lambda x: frequencies[x], reverse=True)
    
    codes = {char: "" for char in sorted_chars}

    def split_and_assign(chars):
        if len(chars) <= 1:
            return
        
        # Ищем точку разделения, чтобы разница сумм частот была минимальной
        total = sum(frequencies[c] for c in chars)
        current_sum = 0
        split_index = 0
        min_diff = float('inf')
        
        for i in range(len(chars) - 1):
            current_sum += frequencies[chars[i]]
            diff = abs(total - 2 * current_sum)
            if diff < min_diff:
                min_diff = diff
                split_index = i + 1
                
        left_part = chars[:split_index]
        right_part = chars[split_index:]
        
        for c in left_part:
            codes[c] += "0"
        for c in right_part:
            codes[c] += "1"
            
        split_and_assign(left_part)
        split_and_assign(right_part)

    split_and_assign(sorted_chars)
    return codes

def build_huffman_code(frequencies):
    """Строит код Хаффмана."""
    heap = [[weight, [char, ""]] for char, weight in frequencies.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    
    codes = {}
    if heap:
        for char, code in heap[0][1:]:
            codes[char] = code
    return codes

# --- Основная логика ---

def process_text(filename):
    print(f"\n--- Обработка файла: {filename} ---")
    
    # Чтение файла (обработка возможных ошибок кодировки)
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='cp1251') as f:
            text = f.read()

    # 1. Посимвольное распределение частот
    # Согласно заданию: заглавные буквы, знаки препинания и пробел считаются отдельными символами.
    # Мы НЕ приводим текст к нижнему регистру.
    counter = Counter(text)
    total_chars = len(text)
    
    # Создаем словарь относительных частот
    frequencies = {char: count / total_chars for char, count in counter.items()}
    # Сортируем для красоты вывода
    sorted_freq = dict(sorted(frequencies.items(), key=lambda item: item[1], reverse=True))

    # 2. Выборочная энтропия
    entropy = get_entropy(list(sorted_freq.values()))
    
    # 3. Построение кодов
    alphabet = sorted(frequencies.keys())
    
    code_uniform = build_uniform_code(alphabet)
    code_sf = build_shannon_fano_code(frequencies)
    code_huff = build_huffman_code(frequencies)

    # 4. Вычисление средней длины
    avg_len_uniform = calculate_average_length(code_uniform, frequencies)
    avg_len_sf = calculate_average_length(code_sf, frequencies)
    avg_len_huff = calculate_average_length(code_huff, frequencies)

    # 5. Кодирование текста
    encoded_uniform = "".join(code_uniform[c] for c in text)
    encoded_sf = "".join(code_sf[c] for c in text)
    encoded_huff = "".join(code_huff[c] for c in text)

    # Сохранение закодированных текстов
    base_name = os.path.splitext(filename)[0]
    
    with open(f"{base_name}_uniform_encoded.txt", "w", encoding='utf-8') as f:
        f.write(encoded_uniform)
    with open(f"{base_name}_shannon_fano_encoded.txt", "w", encoding='utf-8') as f:
        f.write(encoded_sf)
    with open(f"{base_name}_huffman_encoded.txt", "w", encoding='utf-8') as f:
        f.write(encoded_huff)

    # Сохранение таблицы кодировки
    with open(f"{base_name}_codes.txt", "w", encoding='utf-8') as f:
        f.write(f"Таблица кодировки для текста: {filename}\n")
        f.write(f"{'Символ':<10} | {'Частота':<10} | {'Равномерный':<15} | {'Шеннон-Фано':<15} | {'Хаффман':<15}\n")
        f.write("-" * 75 + "\n")
        for char in alphabet:
            # Отображаем пробел и enter красиво
            display_char = repr(char)[1:-1] if char in ' \n\t' else char
            f.write(f"{display_char:<10} | {frequencies[char]:.6f}   | {code_uniform[char]:<15} | {code_sf[char]:<15} | {code_huff[char]:<15}\n")

    # Возвращаем метрики для сравнения
    return {
        "name": filename,
        "entropy": entropy,
        "char_count": total_chars,
        "avg_len_uniform": avg_len_uniform,
        "avg_len_sf": avg_len_sf,
        "avg_len_huff": avg_len_huff,
        "alphabet": alphabet,
        "codes": {
            "uniform": code_uniform,
            "sf": code_sf,
            "huff": code_huff
        },
        "text": text
    }

def cross_encode_and_analyze(text, foreign_codes, code_name, original_name):
    """Кодирует текст 'чужими' кодами."""
    encoded = ""
    missing_chars = set()
    
    for char in text:
        if char in foreign_codes:
            encoded += foreign_codes[char]
        else:
            # Если символа нет в чужом алфавите, мы не можем его закодировать.
            # Для чистоты эксперимента пропускаем или заменяем, но в задании подразумевается, 
            # что алфавиты могут не совпадать.
            missing_chars.add(char)
            pass 
            
    return len(encoded), missing_chars

# --- Запуск ---

def main():
    files = ["Братья Карамазовы.txt", "Война и мир.txt"]
    results = []

    # Проверка наличия файлов
    for f in files:
        if not os.path.exists(f):
            print(f"ОШИБКА: Файл {f} не найден в папке с программой.")
            return

    # Обрабатываем оба текста
    for file in files:
        results.append(process_text(file))

    # --- Анализ и сравнение (Вывод в консоль) ---
    
    print("\n\n" + "="*50)
    print("АНАЛИЗ РЕЗУЛЬТАТОВ")
    print("="*50)

    for res in results:
        print(f"\nТекст: {res['name']}")
        print(f"  Энтропия: {res['entropy']:.4f} бит/символ")
        print(f"  Ср. длина (Равномерный): {res['avg_len_uniform']:.4f} бит")
        print(f"  Ср. длина (Шеннон-Фано): {res['avg_len_sf']:.4f} бит")
        print(f"  Ср. длина (Хаффман):     {res['avg_len_huff']:.4f} бит")
        
        # Оценка эффективности
        best_len = min(res['avg_len_uniform'], res['avg_len_sf'], res['avg_len_huff'])
        print(f"  Наиболее эффективный код: {'Равномерный' if best_len == res['avg_len_uniform'] else 'Шеннона-Фано' if best_len == res['avg_len_sf'] else 'Хаффмана'}")

    # Сравнение "своими" и "чужими" кодами
    print("\n--- Кодирование 'чужими' кодами ---")
    
    text1 = results[0]['text']
    text2 = results[1]['text']
    codes1 = results[0]['codes']
    codes2 = results[1]['codes']

    # 1. Кодируем первый текст кодами Хаффмана/Шеннона-Фано второго текста
    # В задании сказано "кодами ... построенными для второго текста"
    # Для простоты возьмем код Хаффмана, так как он самый эффективный
    
    print(f"\nКодирование '{results[0]['name']}' кодом Хаффмана от '{results[1]['name']}':")
    len_cross_1, missing_1 = cross_encode_and_analyze(text1, codes2['huff'], "Huffman Cross", results[0]['name'])
    print(f"  Длина закодированного текста: {len_cross_1} бит")
    if missing_1:
        print(f"  Внимание: {len(missing_1)} символов отсутствовали в чужом алфавите (пропущены).")
    
    print(f"\nКодирование '{results[1]['name']}' кодом Хаффмана от '{results[0]['name']}':")
    len_cross_2, missing_2 = cross_encode_and_analyze(text2, codes1['huff'], "Huffman Cross", results[1]['name'])
    print(f"  Длина закодированного текста: {len_cross_2} бит")
    if missing_2:
        print(f"  Внимание: {len(missing_2)} символов отсутствовали в чужом алфавите (пропущены).")

    print("\n--- Вывод ---")
    print("1. Коды Хаффмана и Шеннона-Фано дают выигрыш по сравнению с равномерным кодом, приближаясь к энтропии.")
    print("2. Код Хаффмана обычно дает наименьшую среднюю длину (оптимальный префиксный код).")
    print("3. При кодировании 'чужими' кодами эффективность падает (длина растет), так как частоты символов в разных текстах различаются, и чужой код не оптимален для данного распределения. Кроме того, часть символов может вообще отсутствовать в чужом алфавите.")
    print("\nФайлы с таблицами кодировок и закодированными текстами сохранены в папке.")

if __name__ == "__main__":
    main()
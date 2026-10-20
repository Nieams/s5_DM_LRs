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

def cross_encode_and_analyze(text, foreign_codes, native_avg_len, filename_to_save):
    """Кодирует текст 'чужими' кодами и сохраняет результат в файл."""
    encoded = ""
    missing_chars = set()
    encoded_chars_count = 0 # Считаем, сколько символов реально закодировали
    
    for char in text:
        if char in foreign_codes:
            encoded += foreign_codes[char]
            encoded_chars_count += 1
        else:
            missing_chars.add(char)
            
    # Сохраняем файл
    with open(filename_to_save, "w", encoding='utf-8') as f:
        f.write(encoded)
        
    total_bits = len(encoded)
    # Считаем среднюю длину для тех символов, которые закодировались
    cross_avg_len = total_bits / encoded_chars_count if encoded_chars_count > 0 else 0
            
    return total_bits, cross_avg_len, missing_chars

# --- Запуск ---

def main():
    files = ["Братья Карамазовы.txt", "Война и мир.txt"]
    results = []

    for f in files:
        if not os.path.exists(f):
            print(f"ОШИБКА: Файл {f} не найден в папке с программой.")
            return

    for file in files:
        results.append(process_text(file))

    # --- Анализ и сравнение ---
    print("\n\n" + "="*50)
    print("АНАЛИЗ РЕЗУЛЬТАТОВ")
    print("="*50)

    for res in results:
        print(f"\nТекст: {res['name']}")
        print(f"  Энтропия: {res['entropy']:.4f} бит/символ")
        print(f"  Ср. длина (Равномерный): {res['avg_len_uniform']:.4f} бит")
        print(f"  Ср. длина (Шеннон-Фано): {res['avg_len_sf']:.4f} бит")
        print(f"  Ср. длина (Хаффман):     {res['avg_len_huff']:.4f} бит")

    print("\n--- Кодирование 'чужими' кодами ---")
    
    text1 = results[0]['text']
    text2 = results[1]['text']
    codes1 = results[0]['codes']
    codes2 = results[1]['codes']

    # 1. Кодируем первый текст кодом Хаффмана второго текста
    print(f"\nКодирование '{results[0]['name']}' кодом Хаффмана от '{results[1]['name']}':")
    cross_filename_1 = f"{os.path.splitext(results[0]['name'])[0]}_cross_huffman_from_{os.path.splitext(results[1]['name'])[0]}.txt"
    
    # Передаем родную среднюю длину Хаффмана первого текста
    len_cross_1, avg_cross_1, missing_1 = cross_encode_and_analyze(
        text1, codes2['huff'], results[0]['avg_len_huff'], cross_filename_1
    )
    
    print(f"  Длина закодированного текста: {len_cross_1} бит")
    print(f"  Ср. длина 'чужого' кода: {avg_cross_1:.4f} бит/символ")
    print(f"  Ср. длина 'своего' кода (Хаффман): {results[0]['avg_len_huff']:.4f} бит/символ")
    print(f"  Разница (насколько хуже): +{avg_cross_1 - results[0]['avg_len_huff']:.4f} бит на символ")
    
    if missing_1:
        print(f"  Внимание: {len(missing_1)} уникальных символов отсутствовали (пропущены).")
    
    # 2. Кодируем второй текст кодом Хаффмана первого текста
    print(f"\nКодирование '{results[1]['name']}' кодом Хаффмана от '{results[0]['name']}':")
    cross_filename_2 = f"{os.path.splitext(results[1]['name'])[0]}_cross_huffman_from_{os.path.splitext(results[0]['name'])[0]}.txt"
    
    len_cross_2, avg_cross_2, missing_2 = cross_encode_and_analyze(
        text2, codes1['huff'], results[1]['avg_len_huff'], cross_filename_2
    )
    
    print(f"  Длина закодированного текста: {len_cross_2} бит")
    print(f"  Ср. длина 'чужого' кода: {avg_cross_2:.4f} бит/символ")
    print(f"  Ср. длина 'своего' кода (Хаффман): {results[1]['avg_len_huff']:.4f} бит/символ")
    print(f"  Разница (насколько хуже): +{avg_cross_2 - results[1]['avg_len_huff']:.4f} бит на символ")

    if missing_2:
        print(f"  Внимание: {len(missing_2)} уникальных символов отсутствовали (пропущены).")

if __name__ == "__main__":
    main()
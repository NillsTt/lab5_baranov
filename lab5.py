#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Лабораторная работа: Основы системного программирования
Выполнил: Баранов Степан ТРПО24-1
"""

import os
import sys
import platform
import subprocess
import socket
import time
import threading
import asyncio
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("Установите requests: pip install requests")
    requests = None

try:
    import psutil
except ImportError:
    print("Установите psutil: pip install psutil")
    psutil = None

# Упражнение 1

def exercise1_create_directory():
    """Создание директории по указанному пути"""
    print("Упражнение 1.1: Создание директории")
    
    directory = input("Введите путь для создания директории: ").strip()
    
    if not directory:
        print("Путь не может быть пустым!")
        return
    
    try:
        if os.path.exists(directory):
            print(f"Директория '{directory}' уже существует")
        else:
            os.makedirs(directory, exist_ok=False)
            print(f"Директория '{directory}' успешно создана")
    except PermissionError:
        print(f"Нет прав для создания директории '{directory}'")
    except OSError as e:
        print(f"Ошибка при создании директории: {e}")

def exercise1_list_files():
    """Перечисление всех файлов в директории и поддиректориях"""
    print("Упражнение 1.2: Перечисление файлов в директории")
    
    directory = input("Введите путь к директории для перечисления файлов: ").strip()
    
    if not os.path.exists(directory):
        print(f"Директория '{directory}' не существует")
        return
    
    print(f"\nСодержимое директории '{directory}':")
    
    file_count = 0
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            absolute_path = os.path.abspath(os.path.join(root, file))
            print(f"{absolute_path}")
            file_count += 1
    
    print(f"Всего найдено файлов: {file_count}")

# Упражнение 2

def exercise2_ping():
    """Запуск команды ping для проверки доступности ресурса"""
    print("Упражнение 2.1: Проверка доступности с помощью ping")

    host = input("Введите адрес для проверки (например, google.com): ").strip()
    if not host:
        host = "google.com"
    
    param = "-n" if platform.system().lower() == "windows" else "-c"
    
    try:
        print(f"\nВыполняется ping {host}...")
        result = subprocess.run(
            ["ping", param, "4", host],
            capture_output=True,
            text=True,
            encoding='cp866' if platform.system().lower() == "windows" else 'utf-8'
        )
        
        print("\nРезультат выполнения:")
        print(result.stdout)
        
        if result.returncode == 0:
            print(f"Хост {host} доступен")
        else:
            print(f"Хост {host} недоступен")
            
    except subprocess.SubprocessError as e:
        print(f"Ошибка при выполнении ping: {e}")

def exercise2_list_directory():
    """Выполнение команды ls/dir и подсчет файлов"""
    print("Упражнение 2.2: Подсчет файлов в директории")
    
    if platform.system().lower() == "windows":
        command = ["dir"]
        encoding = 'cp866'
    else:
        command = ["ls", "-la"]
        encoding = 'utf-8'
    
    directory = input("Введите путь к директории (Enter для текущей): ").strip()
    if directory:
        command.append(directory)
    
    try:
        print(f"\nВыполняется команда {' '.join(command)}...")
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding=encoding,
            shell=(platform.system().lower() == "windows")
        )
        
        print("\nРезультат выполнения:")
        print(result.stdout)

        lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        
        if platform.system().lower() == "windows":
            files = [l for l in lines if not any(x in l for x in ['Volume', 'Directory', 'Количество', 'байт'])]
        else:
            files = lines[1:] if lines else lines
            
        print(f"\nКоличество элементов в выводе: {len(files)}")
        
    except subprocess.SubprocessError as e:
        print(f"Ошибка при выполнении команды: {e}")

# Упражнение 3

def exercise3_http_request():
    """Отправка HTTP-запроса и анализ ответа"""
    print("Упражнение 3.1: HTTP-запросы с использованием requests")
    
    url = input("Введите URL для проверки (например, https://www.google.com): ").strip()
    if not url:
        url = "https://www.google.com"
    
    try:
        print(f"\nОтправка запроса к {url}...")
        start_time = time.time()
        response = requests.get(url, timeout=10)
        end_time = time.time()
        
        print("\nАнализ ответа:")
        print(f"  • Статус-код: {response.status_code} - {response.reason}")
        print(f"  • Тип содержимого: {response.headers.get('Content-Type', 'Не указан')}")
        print(f"  • Размер контента: {response.headers.get('Content-Length', len(response.content))} байт")
        print(f"  • Время ответа: {(end_time - start_time)*1000:.2f} мс")
        print(f"  • Сервер: {response.headers.get('Server', 'Не указан')}")
        
        if response.status_code == 200:
            print(f"Сайт доступен")
        elif 400 <= response.status_code < 500:
            print(f"Клиентская ошибка: {response.status_code}")
        elif 500 <= response.status_code < 600:
            print(f"Серверная ошибка: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print(f"Не удается подключиться к {url}. Проверьте подключение к интернету")
    except requests.exceptions.Timeout:
        print(f"Таймаут при подключении к {url}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")

def exercise3_socket():
    """Установка соединения через сокеты"""
    print("Упражнение 3.2: Работа с сокетами")
    
    host = input("Введите хост (например, google.com): ").strip()
    if not host:
        host = "google.com"
    
    port = 80
    
    try:
        print(f"\nПодключение к {host}:{port}...")

        request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\nUser-Agent: Python-Socket\r\n\r\n"

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            s.connect((host, port))
            print(f"Подключение установлено")

            print("Отправка HTTP-запроса...")
            s.sendall(request.encode())

            print("Получение ответа...")
            response = b""
            while True:
                try:
                    part = s.recv(4096)
                    if not part:
                        break
                    response += part
                except socket.timeout:
                    break

            response_str = response.decode('utf-8', errors='ignore')
            lines = response_str.split('\r\n')
            
            if lines:
                status_line = lines[0]
                print(f"\nСтатус-код: {status_line}")
                
                headers = {}
                for line in lines[1:]:
                    if ': ' in line:
                        key, value = line.split(': ', 1)
                        headers[key] = value
                    elif line == '':
                        break
                
                print(f"  • Сервер: {headers.get('Server', 'Не указан')}")
                print(f"  • Content-Type: {headers.get('Content-Type', 'Не указан')}")
                print(f"  • Content-Length: {headers.get('Content-Length', 'Не указан')} байт")
                
    except socket.gaierror:
        print(f"Не удается разрешить имя хоста '{host}'")
    except socket.timeout:
        print(f"Таймаут подключения к {host}")
    except ConnectionRefusedError:
        print(f"Соединение отклонено. Убедитесь, что порт {port} открыт")
    except Exception as e:
        print(f"Ошибка: {e}")

# Упражнение 4

def exercise4_system_info():
    """Отображение информации о системе"""
    print("Упражнение 4.1: Системная информация")
    
    print("\nИнформация о системе:")
    print(f"  • Операционная система: {platform.system()} {platform.release()}")
    print(f"  • Версия ОС: {platform.version()}")
    print(f"  • Архитектура: {platform.machine()}")
    print(f"  • Процессор: {platform.processor() or 'Не определён'}")
    print(f"  • Имя компьютера: {platform.node()}")
    
    print(f"\nИнформация о Python:")
    print(f"  • Версия: {platform.python_version()}")
    print(f"  • Компилятор: {platform.python_compiler()}")
    print(f"  • Реализация: {platform.python_implementation()}")
    
    if psutil:
        print(f"\nИнформация о диске:")
        
        if platform.system().lower() == "windows":
            current_drive = os.path.splitdrive(os.getcwd())[0] + '\\'
            disk_path = current_drive
        else:
            disk_path = '/'
        
        try:
            disk_usage = psutil.disk_usage(disk_path)
            print(f"  • Диск: {disk_path}")
            print(f"  • Всего: {disk_usage.total / (1024**3):.2f} GB")
            print(f"  • Использовано: {disk_usage.used / (1024**3):.2f} GB")
            print(f"  • Свободно: {disk_usage.free / (1024**3):.2f} GB")
            print(f"  • Использовано (%): {disk_usage.percent}%")
        except Exception as e:
            print(f"  • Ошибка получения информации о диске: {e}")
        
        print(f"\nИнформация о памяти:")
        try:
            memory = psutil.virtual_memory()
            print(f"  • Всего RAM: {memory.total / (1024**3):.2f} GB")
            print(f"  • Использовано: {memory.used / (1024**3):.2f} GB")
            print(f"  • Свободно: {memory.available / (1024**3):.2f} GB")
            print(f"  • Использовано (%): {memory.percent}%")
        except Exception as e:
            print(f"  • Ошибка получения информации о памяти: {e}")
    else:
        print(f"\nУстановите psutil для подробной информации о системе")
        print(f"   Выполните команду: pip install psutil")

def exercise4_working_directory():
    """Работа с рабочим каталогом и переменными окружения"""
    print("\n" + "="*50)
    print("Упражнение 4.2: Рабочий каталог и переменные окружения")
    print("="*50)
    
    print(f"\nТекущий рабочий каталог: {os.getcwd()}")
    
    test_dir = os.path.join(os.getcwd(), "test_system_dir")
    try:
        os.makedirs(test_dir, exist_ok=True)
        print(f"Создана тестовая директория: {test_dir}")
        
        os.chdir(test_dir)
        print(f"Изменен каталог на: {os.getcwd()}")

        os.chdir('..')
        print(f"Возврат в: {os.getcwd()}")
        
        os.rmdir(test_dir)
        print(f"Удалена тестовая директория")
    except Exception as e:
        print(f"Ошибка при работе с каталогом: {e}")
    
    print(f"\nПеременные окружения (первые 10):")
    for i, (key, value) in enumerate(list(os.environ.items())[:10]):
        value_str = str(value)
        if len(value_str) > 60:
            value_str = value_str[:57] + "..."
        print(f"  • {key} = {value_str}")
    
    important_vars = ['PATH', 'HOME', 'USERNAME', 'USER', 'PYTHONPATH', 'TEMP', 'TMP']
    print(f"\nВажные переменные окружения:")
    for var in important_vars:
        value = os.environ.get(var, 'Не установлена')
        if len(value) > 60:
            value = value[:57] + "..."
        print(f"  • {var} = {value}")

# Упражнение 5

def long_task(name, duration=2):
    """Функция, симулирующая длительную задачу"""
    print(f"Задача '{name}' началась в {datetime.now().strftime('%H:%M:%S')}")
    time.sleep(duration)
    print(f"Задача '{name}' завершилась в {datetime.now().strftime('%H:%M:%S')}")
    return f"Результат задачи {name}"

def exercise5_multithreading():
    """Многопоточное выполнение задач"""
    print("Упражнение 5.1: Многопоточность")

    num_threads = int(input("Введите количество потоков (по умолчанию 5): ") or "5")
    
    print(f"\nЗапуск {num_threads} потоков...")
    start_time = time.time()
    
    threads = []
    results = [None] * num_threads
    
    def task_wrapper(index, name):
        results[index] = long_task(name)
    
    for i in range(num_threads):
        t = threading.Thread(target=task_wrapper, args=(i, f"Поток-{i+1}"))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    end_time = time.time()
    
    print(f"\nВсе задачи выполнены за {(end_time - start_time):.2f} секунд")
    print(f"Полученные результаты: {results}")

async def async_long_task(name, duration=2):
    """Асинхронная функция, симулирующая длительную задачу"""
    print(f"Асинхронная задача '{name}' началась в {datetime.now().strftime('%H:%M:%S')}")
    await asyncio.sleep(duration)
    print(f"Асинхронная задача '{name}' завершилась в {datetime.now().strftime('%H:%M:%S')}")
    return f"Результат асинхронной задачи {name}"

async def exercise5_async():
    """Асинхронное выполнение задач"""
    print("Упражнение 5.2: Асинхронное программирование")
    
    num_tasks = int(input("Введите количество асинхронных задач (по умолчанию 5): ") or "5")
    
    print(f"\nЗапуск {num_tasks} асинхронных задач...")
    start_time = time.time()
    
    tasks = [async_long_task(f"Задача-{i+1}") for i in range(num_tasks)]
    
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    
    print(f"\nВсе асинхронные задачи выполнены за {(end_time - start_time):.2f} секунд")
    print(f"Полученные результаты: {results}")

# main()

def main():
    """Главная функция для запуска всех упражнений"""
    
    exercises = {
        '1': ('Работа с файловой системой', exercise1_create_directory, exercise1_list_files),
        '2': ('Работа с процессами', exercise2_ping, exercise2_list_directory),
        '3': ('Работа с сетями', exercise3_http_request, exercise3_socket),
        '4': ('Работа с системной информацией', exercise4_system_info, exercise4_working_directory),
        '5': ('Многопоточность и асинхронность', exercise5_multithreading, None),
        '6': ('Асинхронное программирование', None, None)
    }
    
    while True:
        print("Упражнения:")
        print("1. Упражнение 1 - Работа с файловой системой")
        print("2. Упражнение 2 - Работа с процессами")
        print("3. Упражнение 3 - Работа с сетями")
        print("4. Упражнение 4 - Работа с системной информацией")
        print("5. Упражнение 5.1 - Многопоточность")
        print("6. Упражнение 5.2 - Асинхронность")
        print("0. Выход")
        
        choice = input("\nВыберите упражнение (0-6): ").strip()
        
        if choice == '0':
            print("\nДо свидания")
            break
        elif choice == '1':
            exercise1_create_directory()
            exercise1_list_files()
        elif choice == '2':
            exercise2_ping()
            exercise2_list_directory()
        elif choice == '3':
            exercise3_http_request()
            exercise3_socket()
        elif choice == '4':
            exercise4_system_info()
            exercise4_working_directory()
        elif choice == '5':
            exercise5_multithreading()
        elif choice == '6':
            asyncio.run(exercise5_async())
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
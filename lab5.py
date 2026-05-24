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
import requests
import socket
import time
import threading
import asyncio
from pathlib import Path
from datetime import datetime

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
        print(f"❌ Ошибка при выполнении ping: {e}")

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


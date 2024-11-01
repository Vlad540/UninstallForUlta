import subprocess
import os
import winreg
import ctypes
import sys

SERVICE_NAME = "Ulta-service"
PROCESS_NAME = "Ulta.exe"
FOLDER_PATH = r"C:\Program Files\Ulta"
REGISTRY_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{6083aade-237d-494e-91c9-3f738c142b75}"
REGISTRY_KEY2 = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{7336be3e-a3e4-4c9b-bf32-123b983b7226}"

def is_admin():
    """Проверка, запущен ли скрипт от имени администратора."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def run_command(command):
    """Запуск командной строки с обработкой ошибок."""
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {' '.join(command)}. Код ошибки: {e.returncode}. Сообщение: {e.stderr.strip()}")

def main():
    # Проверка прав администратора
    if not is_admin():
        print("Запуск от имени администратора...")
        subprocess.run(["powershell", "-Command", "Start-Process python -ArgumentList '%s' -Verb RunAs" % __file__])
        return

    # Остановка службы
    print(f"Остановка службы {SERVICE_NAME}...")
    run_command(["sc", "stop", SERVICE_NAME])

    # Удаление службы
    print(f"Удаление службы {SERVICE_NAME}...")
    run_command(["sc", "delete", SERVICE_NAME])

    # Остановка процесса
    print(f"Остановка процесса по имени {PROCESS_NAME}...")
    run_command(["taskkill", "/F", "/IM", PROCESS_NAME])

    # Удаление папки
    print(f"Удаление папки {FOLDER_PATH}...")
    run_command(["rd", "/S", "/Q", FOLDER_PATH])

    # Удаление ключа реестра
    print(f"Удаление ключа реестра {REGISTRY_KEY}...")
    try:
        winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, REGISTRY_KEY)
        print(f"Ключ реестра {REGISTRY_KEY} успешно удален.")
    except FileNotFoundError:
        print(f"Не удалось удалить ключ реестра {REGISTRY_KEY}. Возможно, он защищен. Продолжаем...")
    except Exception as e:
        print(f"Ошибка при удалении ключа реестра {REGISTRY_KEY}: {e}. Продолжаем...")

    print(f"Удаление ключа реестра {REGISTRY_KEY2}...")
    try:
        winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, REGISTRY_KEY2)
        print(f"Ключ реестра {REGISTRY_KEY2} успешно удален.")
    except FileNotFoundError:
        print(f"Не удалось удалить ключ реестра {REGISTRY_KEY2}. Возможно, он защищен. Продолжаем...")
    except Exception as e:
        print(f"Ошибка при удалении ключа реестра {REGISTRY_KEY2}: {e}. Продолжаем...")

    print("Все операции выполнены.")

if __name__ == "__main__":
    main()

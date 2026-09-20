"""
Скрипт автоматического перезапуска бота при любых изменениях в коде (.py или .env).
Запустите этот файл вместо bot.py, если ведёте активную разработку:
    python run_auto_reload.py
"""

import os
import subprocess
import sys
import time

WATCH_EXTENSIONS = (".py", ".env")
IGNORE_DIRS = ("__pycache__", ".git", "venv", ".venv", ".idea", ".vscode")


def get_file_mtimes():
    """Получение времени последней модификации всех отслеживаемых файлов."""
    mtimes = {}
    for root, _, files in os.walk("."):
        if any(ignored in root for ignored in IGNORE_DIRS):
            continue
        for f in files:
            if f.endswith(WATCH_EXTENSIONS):
                filepath = os.path.join(root, f)
                try:
                    mtimes[filepath] = os.stat(filepath).st_mtime
                except OSError:
                    pass
    return mtimes


def main():
    print("=" * 60)
    print("🚀 SleekCode Bot Auto-Reloader запущен!")
    print("📁 Отслеживание файлов .py и .env активировано.")
    print("💡 Любые изменения в файлах автоматически перезапустят бота.")
    print("=" * 60)

    last_mtimes = get_file_mtimes()
    cmd = [sys.executable, "bot.py"]
    process = subprocess.Popen(cmd)

    try:
        while True:
            time.sleep(1)
            current_mtimes = get_file_mtimes()
            if current_mtimes != last_mtimes:
                print("\n" + "=" * 60)
                print("🔄 Обнаружены изменения в файлах! Автоматический перезапуск...")
                print("=" * 60)

                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()

                last_mtimes = current_mtimes
                process = subprocess.Popen(cmd)
    except KeyboardInterrupt:
        print("\n🛑 Остановка авто-перезапуска и бота...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        print("👋 Бот полностью остановлен.")


if __name__ == "__main__":
    main()

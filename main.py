# main.py
import sys, os, io, zipfile, subprocess, requests
from packaging import version
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui     import QFontDatabase, QFont

# 1. Версия вашего приложения — обнов перед новым релизом!
__version__ = "0.0.1"

# 2. GitHub-репо
GITHUB_REPO = "JJKenn3dy/automatization"

def check_for_updates() -> None:
    api = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    try:
        r = requests.get(api, timeout=10); r.raise_for_status()
    except:
        return
    data = r.json()
    latest = data.get("tag_name","").lstrip("v")
    if not latest or version.parse(latest) <= version.parse(__version__):
        return

    # найдём ZIP-ассет
    zip_url = None
    for a in data.get("assets",[]):
        if a["name"].endswith(".zip"):
            zip_url = a["browser_download_url"]
            break
    if not zip_url:
        return

    # скачиваем и распаковываем
    resp = requests.get(zip_url, timeout=30); resp.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(resp.content))
    tmp = "update_tmp"
    if os.path.isdir(tmp):
        for f in os.listdir(tmp):
            os.remove(os.path.join(tmp,f))
    else:
        os.makedirs(tmp)
    z.extractall(tmp)

    # найдём новый exe и заменим текущий
    new_exe = next(f for f in os.listdir(tmp) if f.lower().endswith(".exe"))
    new_path = os.path.join(tmp, new_exe)
    cur = sys.executable

    # Windows: дождёмся выхода и заменим файл
    cmd = f'timeout /T 1 >nul & move /Y "{new_path}" "{cur}"'
    subprocess.Popen(["cmd","/C",cmd], shell=True)
    sys.exit(0)

def main() -> None:
    check_for_updates()

    app = QApplication(sys.argv)
    if QFontDatabase.addApplicationFont("ui/fonts/Gilroy-Medium.ttf") != -1:
        f = QFont("Gilroy", 10)
        f.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        app.setFont(f)

    from ui.main_window import MainWindow
    win = MainWindow()
    win.resize(1500,900)
    win.setMinimumSize(1500,900)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

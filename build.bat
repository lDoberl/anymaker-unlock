@echo off
REM Сборка standalone .exe (Windows). Требуется установленный Python с python.org.
python -m pip install --upgrade pyinstaller
python -m PyInstaller --onefile --windowed --name "Anymaker Unlock" anymaker_unlock_gui.py
echo.
echo Готово. Файл: dist\Anymaker Unlock.exe
pause

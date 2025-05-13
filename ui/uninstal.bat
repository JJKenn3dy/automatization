@echo off
setlocal

echo [1/5] Stopping and deleting service…
sc.exe stop MariaDB >nul 2>&1
sc.exe delete MariaDB >nul 2>&1

echo [2/5] Uninstalling MSI package…
msiexec.exe /x {5E06FF57-917B-41B1-845C-5042E7A90D6E} /qn

echo [3/5] Removing files and folders…
rmdir /s /q "C:\Program Files\MariaDB"
rmdir /s /q "C:\ProgramData\MariaDB"  2>nul

echo [4/5] Cleaning Start Menu shortcuts…
rmdir /s /q "%ProgramData%\Microsoft\Windows\Start Menu\Programs\MariaDB 11.7 (x64)" 2>nul

echo [5/5] (Optional) Deleting registry keys…
reg delete "HKLM\SOFTWARE\MariaDB 11.7 (x64)" /f 2>nul
reg delete "HKLM\SOFTWARE\WOW6432Node\MariaDB 11.7 (x64)" /f 2>nul

echo Done. MariaDB полностью удалён.
pause
endlocal

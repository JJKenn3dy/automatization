@echo off
REM ──────────────────────────────────────────────────
REM 0) Проверка UTF-8 и прав администратора
chcp 65001 >nul
NET SESSION >nul 2>&1 || (
  echo [ОШИБКА] Запустите этот скрипт от имени администратора!
  pause
  exit /b 1
)

REM ──────────────────────────────────────────────────
REM 1) Параметры (при желании измените)
set "DOWNLOAD_URL=https://mirror.kumi.systems/mariadb//mariadb-11.7.2/winx64-packages/mariadb-11.7.2-winx64.msi"
set "MSI_NAME=mariadb-11.7.2-winx64.msi"
set "WORKDIR=%~dp0"
set "INSTALL_DIR=C:\Program Files\MariaDB"
set "DATA_DIR=C:\Program Files\MariaDB\data"
set "SERVICE_NAME=MariaDB"
set "ROOT_PW=My$ecureP@ssw0rd"
set "NEW_DB=IB"
set "NEW_USER=newuser"
set "NEW_USER_PW=852456qaz"

REM ──────────────────────────────────────────────────
REM 2) Загрузка MSI
echo [1/6] Скачиваю установщик MariaDB...
pushd "%WORKDIR%"
if exist "%MSI_NAME%" del /q "%MSI_NAME%"
curl -L "%DOWNLOAD_URL%" -o "%MSI_NAME%"
if errorlevel 1 (
  echo [ОШИБКА] Не удалось скачать "%DOWNLOAD_URL%".
  popd & pause & exit /b 1
)
echo [1/6] Загрузка выполнена.

REM ──────────────────────────────────────────────────
REM 3) Удаление старой версии
echo [2/6] Останавливаю и удаляю старую службу MariaDB...
taskkill /f /im mysqld.exe    >nul 2>&1
taskkill /f /im mariadbd.exe  >nul 2>&1
sc stop "%SERVICE_NAME%"      >nul 2>&1
sc delete "%SERVICE_NAME%"    >nul 2>&1
timeout /t 2 >nul
if exist "%INSTALL_DIR%" (
  rmdir /s /q "%INSTALL_DIR%"
  if exist "%INSTALL_DIR%" (
    echo [ОШИБКА] Не удалось удалить "%INSTALL_DIR%". Закройте процессы MariaDB и повторите.
    popd & pause & exit /b 1
  )
)
echo [2/6] Старые файлы удалены.

REM ──────────────────────────────────────────────────
REM 4) Установка MariaDB
echo [3/6] Устанавливаю MariaDB...
msiexec /i "%WORKDIR%%MSI_NAME%" /qn ^
  INSTALLDIR="%INSTALL_DIR%" ^
  DATADIR="%DATA_DIR%" ^
  SERVICENAME="%SERVICE_NAME%" ^
  PASSWORD="%ROOT_PW%" ^
  ADDLOCAL=MYSQLSERVER,Client,DBInstance ^
  ALLUSERS=1
if errorlevel 1 (
  echo [ОШИБКА] Установка вернула код %ERRORLEVEL%.
  popd & pause & exit /b 1
)
echo [3/6] Установка завершена.

REM ──────────────────────────────────────────────────
REM 5) Настройка БД
echo [4/6] Конфигурирую базу данных...
set "MYSQL_EXE=%INSTALL_DIR%\bin\mysql.exe"
timeout /t 5 >nul

"%MYSQL_EXE%" -u root -p"%ROOT_PW%" -e "CREATE DATABASE %NEW_DB%;"
if errorlevel 1 (
  echo [ОШИБКА] Не удалось создать базу %NEW_DB%.
  popd & pause & exit /b 1
)

"%MYSQL_EXE%" -u root -p"%ROOT_PW%" -e ^
  "GRANT ALL PRIVILEGES ON %NEW_DB%.* TO '%NEW_USER%'@'localhost' IDENTIFIED BY '%NEW_USER_PW%'; FLUSH PRIVILEGES;"
if errorlevel 1 (
  echo [ОШИБКА] Не удалось выдать права пользователю %NEW_USER%.
  popd & pause & exit /b 1
)
echo [4/6] База данных настроена.

REM ──────────────────────────────────────────────────
REM 6) Готово
echo [5/6] Всё успешно! MariaDB установлена, служба запущена.
echo База '%NEW_DB%' и пользователь '%NEW_USER%' готовы.
popd
pause
exit /b 0

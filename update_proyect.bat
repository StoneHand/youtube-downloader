@echo off
REM Trabajar siempre desde la carpeta donde esta este archivo
cd /d "%~dp0"

REM Guardar cambios locales solo si realmente existen (evita restaurar un stash viejo)
set "STASHED=0"
git diff --quiet HEAD
if errorlevel 1 (
    git stash push -m "Backup automatico antes de pull"
    if errorlevel 1 (
        echo Error: Fallo el stash. Por favor, verifica manualmente.
        pause
        exit /b 1
    )
    set "STASHED=1"
)

REM Hacer pull de los ultimos cambios
echo Actualizando el repositorio...
git pull origin main --rebase
if errorlevel 1 (
    echo Error: Fallo el git pull.
    if "%STASHED%"=="1" echo Tus cambios locales siguen guardados en el stash.
    pause
    exit /b 1
)

REM Restaurar los cambios guardados, solo si se guardo algo en este script
if "%STASHED%"=="1" (
    git stash pop
    if errorlevel 1 (
        echo Nota: No se pudo aplicar el stash automaticamente. Los cambios siguen guardados en el stash.
    )
)

echo El proyecto se actualizo correctamente.
pause

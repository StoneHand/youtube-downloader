REM Hacer stash automático si hay cambios sin confirmar
git stash save "Backup automático antes de pull"
if %errorlevel% neq 0 (
    echo Error: Falló el stash. Por favor, verifica manualmente.
    pause
    exit /b 1
)

REM Hacer pull de los últimos cambios
echo Actualizando el repositorio...
git pull origin main --rebase
if %errorlevel% neq 0 (
    echo Error: Falló el git pull.
    pause
    exit /b 1
)

REM Restaurar los cambios del stash si hay algo pendiente
git stash pop
if %errorlevel% neq 0 (
    echo Nota: No se pudo aplicar el stash automáticamente. Los cambios siguen guardados en el stash.
)

echo El proyecto se actualizó correctamente.
pause
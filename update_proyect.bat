REM Hacer pull de los últimos cambios
echo Actualizando el repositorio...
git pull origin main
if %errorlevel% neq 0 (
    echo Error: Falló el git pull, por favor contacte al creador.
    pause
    exit /b 1
)

echo El proyecto se actualizó correctamente.
pause
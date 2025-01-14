REM Hacer pull de los últimos cambios
echo Actualizando el repositorio...
git pull origin main
if %errorlevel% neq 0 (
    echo Error: Falló el git pull.
    pause
    exit /b 1
)

echo El proyecto se actualizó correctamente.
pause
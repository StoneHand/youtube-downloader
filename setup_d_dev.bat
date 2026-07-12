@echo off
setlocal EnableExtensions

set "TARGET_DIR=D:\Dev"
set "REPO_DIR=%TARGET_DIR%\youtube-downloader"
set "BRANCH=cursor/fix-youtube-downloader-4ddd"
set "REPO_URL=https://github.com/StoneHand/youtube-downloader.git"

echo ============================================
echo  YouTube Downloader - Instalacion en D:\Dev
echo ============================================
echo.

if not exist "%TARGET_DIR%" (
    echo Creando carpeta %TARGET_DIR% ...
    mkdir "%TARGET_DIR%"
)

if exist "%REPO_DIR%\.git" (
    echo Actualizando repositorio existente en %REPO_DIR% ...
    pushd "%REPO_DIR%"
    git fetch origin
    git checkout %BRANCH%
    git pull origin %BRANCH%
    if errorlevel 1 (
        echo Error al actualizar el repositorio.
        popd
        pause
        exit /b 1
    )
    popd
) else (
    echo Clonando rama %BRANCH% en %REPO_DIR% ...
    git clone -b %BRANCH% %REPO_URL% "%REPO_DIR%"
    if errorlevel 1 (
        echo Error al clonar el repositorio.
        pause
        exit /b 1
    )
)

pushd "%REPO_DIR%"

echo.
echo Instalando dependencias de Python...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Error al instalar dependencias.
    popd
    pause
    exit /b 1
)

echo.
echo Comprobando herramientas opcionales...
where ffmpeg >nul 2>&1
if errorlevel 1 (
    echo [AVISO] FFmpeg no encontrado en PATH. Instalalo desde https://ffmpeg.org/download.html
) else (
    echo [OK] FFmpeg encontrado.
)

where deno >nul 2>&1
if errorlevel 1 (
    where node >nul 2>&1
    if errorlevel 1 (
        echo [AVISO] Deno/Node no encontrado. Recomendado para YouTube: https://docs.deno.com/runtime/
    ) else (
        echo [OK] Node.js encontrado.
    )
) else (
    echo [OK] Deno encontrado.
)

echo.
echo ============================================
echo  Instalacion completada
echo  Carpeta: %REPO_DIR%
echo ============================================
echo.
echo Para ejecutar:
echo   cd /d %REPO_DIR%
echo   python main.py
echo.
echo Si YouTube pide verificacion:
echo   set YTDLP_COOKIES_BROWSER=chrome
echo   python main.py
echo.

popd
pause

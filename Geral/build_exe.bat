@echo off
setlocal

where py >nul 2>&1
if errorlevel 1 (
    set "PYTHON=python"
) else (
    set "PYTHON=py"
)

%PYTHON% -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo PyInstaller nao encontrado. Instalando...
    %PYTHON% -m pip install pyinstaller
    if errorlevel 1 (
        echo Falha ao instalar o PyInstaller.
        exit /b 1
    )
)

%PYTHON% -m PyInstaller --noconfirm --clean --onefile --windowed --name Circuita main.py
if errorlevel 1 (
    echo Falha ao criar o executavel.
    exit /b 1
)

echo.
echo Executavel criado em dist\Circuita.exe

@echo off
echo ========================================
echo      SmartBudget - Dashboard Financeiro
echo           Iniciando aplicacao...
echo ========================================
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale Python 3.7+ de https://python.org
    echo.
    pause
    exit /b 1
)

echo Python encontrado! Verificando dependencias...
echo.

REM Instalar dependencias automaticamente
echo Instalando/Verificando bibliotecas necessarias...
pip install pandas matplotlib numpy tkinter-tooltip >nul 2>&1

if errorlevel 1 (
    echo.
    echo Tentando instalacao alternativa...
    python -m pip install pandas matplotlib numpy >nul 2>&1
)

echo.
echo Iniciando SmartBudget...
echo.

REM Executar aplicacao
python SmartBudget.py

REM Se houve erro, mostrar mensagem
if errorlevel 1 (
    echo.
    echo ========================================
    echo     ERRO ao executar SmartBudget!
    echo ========================================
    echo.
    echo Possiveis solucoes:
    echo 1. Verifique se o arquivo SmartBudget.py esta na mesma pasta
    echo 2. Execute manualmente: python SmartBudget.py
    echo 3. Instale dependencias: pip install pandas matplotlib numpy
    echo.
    pause
) else (
    echo.
    echo SmartBudget finalizado com sucesso!
)

pause
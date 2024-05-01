@echo off
cls
echo.
set /p palabra="Introduce la palabra a buscar: "
echo Buscando la palabra "%palabra%" en todos los archivos .txt en la ruta especificada...
echo.
cd /d E:\Documentos\01. ESCUELA POLITECNICA NACIONAL\08. EPN 8\2. RECUPERACION DE LA INFORMACION\Tareas\B1\01\Data
echo Archivos que contienen la palabra "%palabra%":
echo ----------------------------------------------------
findstr /S /I /M "%palabra%" *.txt
echo ----------------------------------------------------
if errorlevel 1 (
    echo No se encontraron resultados.
) else (
    echo Resultado: Los archivos listados arriba contienen la palabra buscada.
)
echo.
pause

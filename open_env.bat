@echo off

:: Check if %0 is %~nx0 and if not, start a new cmd window and exit this one
:: %0 is the name of the batch file with the path
:: %~nx0 is the name of the batch file without the path
:: %0 == %~nx0 is true if the batch file was started without a path
if not %0 == %~nx0 (
    echo Opening a new window to run the script...
    timeout 1
    start cmd /k %~nx0
    exit
)

echo Starting the environment...
call .venv\Scripts\activate.bat

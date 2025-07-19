@echo off
REM RaffleManager Data Generator - Windows Batch File
REM Usage: generate.bat <blank> <roster> <mail> <mixed> [filename] [ticket_cost]

if "%4"=="" (
    echo Usage: generate.bat ^<blank_count^> ^<roster_count^> ^<mail_count^> ^<mixed_count^> [filename] [ticket_cost]
    echo.
    echo Examples:
    echo   generate.bat 5 10 15 20
    echo   generate.bat 100 0 0 0 large_blank.lua
    echo   generate.bat 0 0 50 0 mail_only.lua 500
    echo   generate.bat 10 20 30 40 custom.lua 1500
    echo.
    goto :eof
)

set BLANK_COUNT=%1
set ROSTER_COUNT=%2
set MAIL_COUNT=%3
set MIXED_COUNT=%4

REM Build the command based on what parameters are provided
set CMD=python generate_raffle_data.py %BLANK_COUNT% %ROSTER_COUNT% %MAIL_COUNT% %MIXED_COUNT%

if not "%5"=="" (
    if not "%6"=="" (
        REM Both filename and ticket_cost provided
        set CMD=%CMD% --filename %5 --ticket-cost %6
    ) else (
        REM Check if %5 is a number (ticket_cost) or filename
        echo %5| findstr /r "^[0-9][0-9]*$" >nul
        if errorlevel 1 (
            REM %5 is not a number, treat as filename
            set CMD=%CMD% --filename %5
        ) else (
            REM %5 is a number, treat as ticket_cost
            set CMD=%CMD% --ticket-cost %5
        )
    )
)

%CMD%

if %ERRORLEVEL% EQU 0 (
    echo.
    echo File generated successfully!
) else (
    echo.
    echo Error occurred during generation.
)

pause

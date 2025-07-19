@echo off
REM RaffleManager Data Generator - Windows Batch File
REM Usage: generate.bat <blank> <roster> <mail> <mixed> [filename]

if "%4"=="" (
    echo Usage: generate.bat ^<blank_count^> ^<roster_count^> ^<mail_count^> ^<mixed_count^> [filename]
    echo.
    echo Examples:
    echo   generate.bat 5 10 15 20
    echo   generate.bat 100 0 0 0 large_blank.lua
    echo   generate.bat 0 0 50 0 mail_only.lua
    echo.
    goto :eof
)

set BLANK_COUNT=%1
set ROSTER_COUNT=%2
set MAIL_COUNT=%3
set MIXED_COUNT=%4

if "%5"=="" (
    python generate_raffle_data.py %BLANK_COUNT% %ROSTER_COUNT% %MAIL_COUNT% %MIXED_COUNT%
) else (
    python generate_raffle_data.py %BLANK_COUNT% %ROSTER_COUNT% %MAIL_COUNT% %MIXED_COUNT% --filename %5
)

if %ERRORLEVEL% EQU 0 (
    echo.
    echo File generated successfully!
) else (
    echo.
    echo Error occurred during generation.
)

pause

@echo off

rem Install packages using pip
pip install matplotlib Tk requests bs4

rem Check if installation was successful
if %errorlevel% equ 0 (
  echo Installation successful
) else (
  echo Installation failed
)
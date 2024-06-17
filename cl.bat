@echo off
set ORIGIN=%CD%
cd /d %~dp0
call .venv\Scripts\activate.bat
python -m cl %*
cd /d %ORIGIN%
deactivate

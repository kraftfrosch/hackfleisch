@echo off

:: Activate conda environment
call conda activate cdtmhack

:: Get the directory of the script
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."

:: Change to the project root directory
cd /d "%PROJECT_ROOT%"

:: Start the video agent
python src/external_agents/video_agent.py start 
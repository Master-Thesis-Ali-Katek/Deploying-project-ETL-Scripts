@echo off
:: Set script to run from the current directory
cd /d %~dp0

:: Define variables
set CONTAINER_NAME=pb-smt-container
set IMAGE_NAME=pb-smt-automation
set LOCAL_FILES_PATH=C:/Users/PATANS/Downloads/pb_smt_automation/New folder
set OUTPUTS_PATH=C:/Users/PATANS/Downloads/pb_smt_automation/pb_smt_data_automation/processed_outputs

:: Remove any existing container with the same name
docker rm -f %CONTAINER_NAME% >nul 2>&1

:: Run Docker container with volume mapping
docker run --rm -it --name %CONTAINER_NAME% ^
    -v "%LOCAL_FILES_PATH%:/local_files" ^
    -v "%OUTPUTS_PATH%:/main/pb_smt_data_automation/processed_outputs" ^
    %IMAGE_NAME%

:: Exit script
exit

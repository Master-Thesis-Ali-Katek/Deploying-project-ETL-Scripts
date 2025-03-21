@echo off
echo Starting Docker Container for Kapa Automation...
docker run --rm -it ^
    -v "C:/Users/PATANS/Downloads/kapa_automation:/main" ^
    -v "C:/Users/PATANS/Downloads/pb_smt_automation/pb_smt_data_automation/processed_outputs:/processed_outputs" ^
    kapa-automation-app
echo Docker Container Execution Completed.
pause

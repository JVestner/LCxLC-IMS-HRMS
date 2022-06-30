ECHO ON
set root=C:\ProgramData\Anaconda3
call %root%\Scripts\activate.bat %root%

call conda activate lclcimapp

call python main.py

@ECHO ---------------------------------------------------------------------
@ECHO ---------------------------------------------------------------------

pause

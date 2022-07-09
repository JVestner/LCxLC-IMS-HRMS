ECHO ON
set root=C:\ProgramData\Anaconda3
call %root%\Scripts\activate.bat %root%
@rem call conda env list
dir

call conda create --name lclcimapp --yes
call conda activate lclcimapp
call conda install -c anaconda numpy --yes
call conda install -c anaconda pandas --yes
call conda install -c conda-forge dash --yes
call conda install -c conda-forge dash-core-components --yes
call conda install -c conda-forge dash-html-components --yes
call conda install -c bioconda pyteomics --yes
call conda install -c conda-forge dash-renderer --yes



@ECHO -----------------------------------------------
@ECHO ----------------------DONE---------------------
@ECHO -----------------------------------------------

pause

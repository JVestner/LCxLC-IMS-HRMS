ECHO ON
set root=C:\ProgramData\Anaconda3
call %root%\Scripts\activate.bat %root%
@rem call conda env list
dir

call conda create --name lclcimapp --yes
call conda activate lclcimapp
call conda install -c anaconda numpy=1.15 --yes
call conda install -c anaconda pandas=0.23 --yes
call conda install -c conda-forge dash=0.26 --yes
call conda install -c conda-forge dash-core-components=0.28 --yes
call conda install -c conda-forge dash-html-components=0.12 --yes
call conda install -c bioconda pyteomics=3.5 --yes
call conda install -c conda-forge dash-renderer=0.13 --yes



@ECHO -----------------------------------------------
@ECHO ----------------------DONE---------------------
@ECHO -----------------------------------------------

pause

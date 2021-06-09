## Contains the source code for push_to_git.exe
## Why: A .bat file opens a windows when run, a .exe file does not
cd D:\JupyterNotebooks\covid_automated_dashboard\
git pull
git add --all
git commit -m "Auto commit on %date:~0,2%/%date:~3,2%/%date:~-4% at %time:~0,2%:%time:~3,2%"
git push
exit

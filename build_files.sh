echo "BUILD START"
C:\users\hp\appdata\local\programs\python\python38\python.exe -m pip install -r requirements.txt
C:\users\hp\appdata\local\programs\python\python38\python.exe manage.py collectstatic  --noinput --clear 
echo "BUILD END"
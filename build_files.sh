echo "BUILD START"
env\Scripts\activate
python3.8 -m pip install -r requirements.txt
python3.8 manage.py collectstatic  --noinput --clear 
deactivate
echo "BUILD END"
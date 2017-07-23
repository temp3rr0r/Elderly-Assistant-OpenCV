source ~/.profile
workon cv 
python dishes.py &
FLASK_APP=flaskRestful.py flask run --host=0.0.0.0 &

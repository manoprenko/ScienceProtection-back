killall gunicorn
gunicorn -b 0.0.0.0:8000 -w 4 server:app

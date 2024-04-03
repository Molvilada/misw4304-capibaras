# Entrypoint for the Elastic Beanstalk WSGI server
from app import create_app

application = create_app('sqlite:///db.sqlite')

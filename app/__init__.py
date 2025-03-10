import eventlet
eventlet.monkey_patch()
from flask import Flask
from config import Config
from flask_socketio import SocketIO
from celery import Celery

application = Flask(__name__)
application.config.from_object(Config)
application.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
application.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
socketio = SocketIO(application, cors_allowed_origins="*", message_queue='redis://')
celery = Celery(application.name, broker=application.config['CELERY_BROKER_URL'])
celery.conf.update(application.config)


from app import routes






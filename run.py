import eventlet
eventlet.monkey_patch() 
from app import application

if __name__ == '__main__':
    application.run(debug=True)  # Runs the server in debug mode

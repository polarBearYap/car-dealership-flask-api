from os import environ
from car_dealership import app

# Execute only when this module is the main program
if __name__ == '__main__':
    # HOST = environ.get('SERVER_HOST', 'localhost')
    #try:
    #    PORT = int(environ.get('SERVER_PORT', '5555'))
    #except ValueError:
    #    PORT = 5555
    #app.run(HOST, PORT, debug=False)
    app.run(host='0.0.0.0', debug=True)
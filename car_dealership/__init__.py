from flask import Flask
from car_dealership.price.price import car_price_bp

# Create the Flask application object, which contains data about the application and also methods (objsect functions) that tell the application to do certain actions. The last line, app.run(), is one such method.
app = Flask(__name__)

app.register_blueprint(car_price_bp)

import car_dealership.main
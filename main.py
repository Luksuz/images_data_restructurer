from flask import Flask, request
from Configurator import Configurator
app = Flask(__name__)
PORT = 8080

configurator = Configurator()

@app.route('/train_test', methods=['POST'])
def train_test():

    zip_file = request.files["data"]
    data = request.form
    dimensions, grayscale, structure = data.get('dimensions').split(","), data.get('grayscale'), data.get('structure')

    response = configurator.train_test(zip_file, dimensions, grayscale, structure)

    return response

@app.route('/train_val_test', methods=['POST'])
def train_val_test():
    
    zip_file = request.files["data"]
    data = request.form
    dimensions, grayscale, structure = data.get('dimensions').split(","), data.get('grayscale'), data.get('structure')

    response = configurator.train_val_test(zip_file, dimensions, grayscale, structure)

    return response




if __name__ == '__main__':
    app.run(port=PORT)
from flask import Flask, jsonify
from units import unit_data
from waves import wave_data
from sends import send_data
import json

app = Flask(__name__)
units_data = unit_data()
wave_data = wave_data()
send_data = send_data()


@app.route('/units/', methods=['GET'])
def get_units():
    return jsonify(units_data)

@app.route('/waves/', methods=['GET'])
def get_waves():
    return jsonify(wave_data)


@app.route('/units/<string:unit>', methods=['GET'])
def get_unit(unit):
    if unit in units_data:
        return jsonify(units_data[unit])
    else:
        return jsonify({"error": "unit does not exist"})


@app.route('/waves/<string:wave>', methods=['GET'])
def get_wave(wave):
    if wave in wave_data:
        return jsonify(wave_data[wave])
    else:
        return jsonify({"error": "wave does not exist"})


@app.route('/waves/number/<string:number>', methods=['GET'])
def get_wave_by_number(number):
    for wave in wave_data:
        if wave_data[wave]['wave'] == number:
            return jsonify(wave_data[wave])

    return jsonify({"error": "wave does not exist"})


if __name__ == '__main__':
    app.run()

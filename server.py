import os
import json
from datetime import datetime
from flask import Flask, jsonify, abort, request, make_response, url_for,redirect,render_template,flash



app = Flask("Smart Bin")

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Unhandled Exception: %s', (e))
    return "Unhandled Error"

@app.route('/getbins', methods=['POST'])
def get_bins():
    if request.method == 'POST':
    	bin_info = request.get_json(force=True)
    	file_name = list(bin_info.keys())[0]
    	with open(file_name + '.json') as f:
    		data = json.load(f)
    		bins = bin_info[file_name]
    		return_json = {}
    		for b in bins:
    			return_json[b] = data[b];
    	return jsonify(return_json)
    	#return jsonify({'bin_size':bin_size, 'bin_id':bin_id, 'articles':articles,'last_emptied_time':last_emptied_time,'location':location,'scanned_items':scanned_items,'unscanned_items':unscanned_items, 'contamination_rate':contamination_rate, 'percent_full':percent_full})
    else:
    	abort(400)

@app.route('/getintegrity', methods=['POST'])
def get_contamination():
    if request.method == 'POST':
    	bin_info = request.get_json(force=True)
    	file_name = list(bin_info.keys())[0]
    	with open(file_name + '.json') as f:
    		data = json.load(f)
    		bins = bin_info[file_name]
    		return_json = {}
    		for b in bins:
    			return_json[b] = {};
    			if (data[b]['scanned_items'] + data[b]['unscanned_items'] == 0):
    				return_json[b]['integrity'] = 0
    			else:
    				return_json[b]['integrity'] = (data[b]['scanned_items']/(data[b]['scanned_items'] + data[b]['unscanned_items']))
    	return jsonify(return_json)
    else:
    	abort(400)


@app.route('/getpercentfull', methods=['POST'])
def get_percent_full():
    if request.method == 'POST':
    	bin_info = request.get_json(force=True)
    	file_name = list(bin_info.keys())[0]
    	with open(file_name + '.json') as f:
    		data = json.load(f)
    		bins = bin_info[file_name]
    		return_json = {}
    		for b in bins:
    			return_json[b] = {};
    			if (data[b]['scanned_items'] + data[b]['unscanned_items'] == 0):
    				return_json[b]['percent_full'] = 0.0
    			else:
    				return_json[b]['percent_full'] = (data[b]['scanned_items'] + data[b]['unscanned_items'])/(data[b]['bin_size'])
    	return jsonify(return_json)
    else:
    	abort(400)


@app.route('/empty', methods=['POST'])
def empty_bins():
    if request.method == 'POST':
    	bin_info = request.get_json(force=True)
    	file_name = list(bin_info.keys())[0]
    	with open(file_name + '.json') as f:
    		data = json.load(f)
    		bins = bin_info[file_name]
    		return_json = {}
    		for b in bins:
    			data[b]['unscanned_items'] = 0
    			data[b]['scanned_items'] = 0
    			data[b]['articles'] = []
    			data[b]['last_emptied_time'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    	with open(file_name + '.json', 'w') as json_file:
    		json.dump(data, json_file)
    	return 'The bin has been emptied'
    else:
    	abort(400)

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)
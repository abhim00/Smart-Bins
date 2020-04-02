import os
from flask import Flask, jsonify, abort, request, make_response, url_for,redirect,render_template,flash
from datetime import datetime
app = Flask("Smart Bin")
bin_size=150
bin_id = 473811
last_emptied_time = datetime.today()
location = "2400 Durant Ave."
scanned_items = 23
unscanned_items = 35
articles = ["glass", "plastic", "unknown","cardboard"]

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
    	if scanned_items + unscanned_items == 0:
    		contamination_rate = 0
    		percent_full = 0
    	else:
	    	contamination_rate = (0.95 * scanned_items) / (scanned_items + unscanned_items)
	    	percent_full = (scanned_items + unscanned_items) / float(bin_size)
    	return jsonify({'bin_size':bin_size, 'bin_id':bin_id, 'articles':articles,'last_emptied_time':last_emptied_time,'location':location,'scanned_items':scanned_items,'unscanned_items':unscanned_items, 'contamination_rate':contamination_rate, 'percent_full':percent_full})
    else:
    	abort(400)

@app.route('/empty', methods=['POST'])
def empty_bins():
    if request.method == 'POST':
    	global last_emptied_time
    	global scanned_items
    	global unscanned_items
    	last_emptied_time = datetime.today()
    	scanned_items = 0
    	unscanned_items = 0
    	return 'The bin has been emptied'
    else:
    	abort(400)

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)

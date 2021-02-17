
from flask import Flask, request
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup
import json
import re

from modules.rightmove import getLetProperty

app = Flask('ts')

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/rightmove', methods=['GET', 'POST'])
@cross_origin()
def rightmove():
	url = request.args.get('url')
	return getLetProperty(url)
	
app.run(debug=True, port=5000)
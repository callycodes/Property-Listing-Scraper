import requests
from bs4 import BeautifulSoup
import json
import re

# Take the page source [page] and selector path [selector], select first element
# and extract text, function for error handling
def getField(page, selector):
	try:
		return page.select(selector)[0].text
	except:
		return ''

# Dictionary holds key:value pair defining json_identifier:css-selector
fieldKeys = {
	'address': 'h1._2uQQ3SV0eMHL1P6t5ZDo2q',
	'price_per_month': 'div._1gfnqJ3Vtd1z40MlC0MzXu > span:nth-child(1)',
	'price_per_week': 'div.HXfWxKgwCdWTESd5VaU73',
	'added': 'div._2fFy6nQs_hX4a6WEDR-B-6 > div._2ooK8ecdlbj0miM4morNpK > div:nth-child(2) > div',
}


lettingKeys = {
	'let_type': 'Let type: ',
	'furnish_type': 'Furnish type: ',
	'let_available': 'Let available date: ',
	'deposit': 'Deposit: '
}


propertyKeys = {
	'property_type': 'PROPERTY TYPE',
	'bedrooms': 'BEDROOMS',
	'bathrooms': 'BATHROOMS'
}

def getLetProperty(url):

	page = requests.get(url)
	page_parsed = BeautifulSoup(page.content, 'html.parser')
	
	meta_parsed = BeautifulSoup(page.text, 'html.parser')
	head_parsed = str(meta_parsed.select('head')[0])
	
	main_photo = page_parsed.select('div._30hgiLFzNTpFG4iV-9f6oK > a > meta')[0]['content']
	
	photo_count = int(page_parsed.select('div._2TqQt-Hr9MN0c0wH7p7Z5p > div._30hgiLFzNTpFG4iV-9f6oK > div._3MkSmDcjGxPAT3dNBKwRQz > a > span')[0].text)
	##for i in range(0, int(photo_count)):
		##photos.append(url + '/media?id=media' + str(i))
	
	
	property_json = {
		'url': '',
		'address': '',
		'price_per_month': '',
		'price_per_week': '',
		'property_info': {},
		'letting_info': {},
		'added': '',
		'realtor': '',
		'stations': [],
		'features': [],
		'photo_count': 0,
		'photo': ''
	}
	
	for fKey in fieldKeys:
		property_json[fKey] = getField(page_parsed, fieldKeys.get(fKey))
	
	letting_details = {
		'let_type': '',
		'furnish_type': '',
		'let_available': '',
		'deposit': ''
	}
	
	property_details = {
		'property_type': '',
		'bedrooms': '',
		'bathrooms': ''
	}
	
	try:
		for div in page_parsed.select('#root > div > div.WJG_W7faYk84nW-6sCBVi > main > div._21Dc_JVLfbrsoEkZYykXK5 > dl')[0]:
			for (fKey, cont) in lettingKeys.items():
				if div.select('div > dt')[0].text in cont:
					print(True)
					letting_details[fKey] = div.select('div > dd')[0].text
	except:
		print('Problem with letting keys')

	for div in page_parsed.select('#root > div > div.WJG_W7faYk84nW-6sCBVi > main > div._4hBezflLdgDMdFtURKTWh')[0]:
		for (fKey, cont) in propertyKeys.items():
			if div.select('div:nth-child(1)')[0].text in cont:
				print(True)
				property_details[fKey] = div.select('div:nth-child(2) > div:nth-child(2)')[0].text
				
	realtor = {
		'name': page_parsed.select('div.WJG_W7faYk84nW-6sCBVi > aside > div > div > div._2WvNKlXUtQjtXXF3acAyQp > div._1HfIlGN38D_5t6P1dlQ4pW > div._2OyLeBVg-z92a2saGVUNnD > div > div.RPNfwwZBarvBLs58-mdN8 > a')[0].text,
		'telephone': page_parsed.select('div.WJG_W7faYk84nW-6sCBVi > aside > div > div > div._2WvNKlXUtQjtXXF3acAyQp > div._1HfIlGN38D_5t6P1dlQ4pW > div._2jlFWdXWxYn37izq_CadDw > div > div > a')[0]['href']
	}
	
	stations = []
	features = []
	
	for feature in page_parsed.select('div.WJG_W7faYk84nW-6sCBVi > main > ul')[0]:
		features.append(feature.text)

	for station in page_parsed.select('div._3v_yn6n1hMx6FsmIoZieCM > div._2CdMEPuAVXHxzb5evl1Rb8 > ul')[0]:
		stations.append({
			'type': station.select('li > div._33FcKz0Izh9IdGj_vDDgmK > svg > use')[0]['xlink:href'],
			'name': station.select('li > div.Hx6myckw6FR-gq2-nskGM > div > span.cGDiWU3FlTjqSs-F1LwK4')[0].text,
			'distance': station.select('li > div.Hx6myckw6FR-gq2-nskGM > div > span._1ZY603T1ryTT3dMgGkM7Lg')[0].text
		})
	
	property_json['realtor'] = realtor
	property_json['stations'] = stations
	property_json['features'] = features
	property_json['photo_count'] = photo_count
	property_json['photo'] = main_photo
	property_json['letting_info'] = letting_details
	property_json['property_info'] = property_details
	
	property_json['url'] = url
	
	return json.dumps(property_json, indent=4, sort_keys=True, ensure_ascii=False)
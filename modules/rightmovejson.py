import requests
from bs4 import BeautifulSoup
import json
import re

class Property:
  id = ''
  info = {
    'bedrooms': 0,
    'bathrooms': 0,
    'type': ''
  }
  prices = {
    'monthly': '',
    'weekly': ''
  }
  location = {
    'display': '',
    'latitude': 0,
    'longitude': 0
  }
  letting = {
    'available': '',
    'deposit': 0,
    'type': '',
    'furnished': ''
  }
  features = []
  images = []
  realtor = {
    'name': '',
    'address': '',
    'logo': '',
    'phone': ''
  }
  stations = []

  def __init__(self, id, info, prices, location, letting, features, images, realtor, stations):
    self.id = id,
    self.info = info
    self.prices = prices
    self.location = location
    self.letting = letting
    self.features = features
    self.images = images
    self.realtor = realtor
    self.stations = stations

def find_between(s, start, end):
  return (s.split(start))[1].split(end)[0]

def scrapeProperty(url):
  try:
    page = requests.get(url)

    json_scraped = find_between(page.text, 'window.PAGE_MODEL = ', '</script>')

    property_obj = json.loads(json_scraped)['propertyData']

    image_index = 0
    images_cleaned = []
    stations_cleaned = []

    for image in property_obj['images']:
      images_cleaned.append({
        'url': image['url'],
        'order': image_index
      })
      image_index = image_index + 1

    for station in property_obj['nearestStations']:
      stations_cleaned.append({
        'name': station['name'],
        'unit': station['unit'],
        'distance': station['distance'],
        'type': station['types'][0]
      })

    property_cleaned = Property(
      id = property_obj['id'],
      info = {
        'bedrooms': property_obj['bedrooms'],
        'bathrooms': property_obj['bathrooms'],
        'type': property_obj['soldPropertyType']
      },
      prices = { 
        'monthly': property_obj['prices']['primaryPrice'],
        'weekly': property_obj['prices']['secondaryPrice']
      },
      location = {
        'display': property_obj['address']['displayAddress'],
        'latitude': property_obj['location']['latitude'],
        'longitude': property_obj['location']['longitude']
      },
      letting = {
        'available': property_obj['lettings']['letAvailableDate'],
        'deposit': property_obj['lettings']['deposit'],
        'type': property_obj['lettings']['letType'],
        'furnished': property_obj['lettings']['furnishType']
      },
      features = property_obj['keyFeatures'],
      images = images_cleaned,
      realtor = {
        'name': property_obj['customer']['branchDisplayName'],
        'address': property_obj['customer']['displayAddress'],
        'logo': property_obj['customer']['logoPath'],
        'phone': property_obj['contactInfo']['telephoneNumbers']['localNumber']
      },
      stations = stations_cleaned
    )
    
    return json.dumps(property_cleaned.__dict__, indent=4, sort_keys=True, ensure_ascii=False)
  except Exception as e:
    error_result = {
      'error': 'Something went wrong'
    }
    print(e)
    return json.dumps(error_result, indent=4, sort_keys=True, ensure_ascii=False)
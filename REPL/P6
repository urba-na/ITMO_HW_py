#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 19:18:14 2026

@author: nadya_urba
"""

from zip_util import read_zip_all
import math

LOC = 'loc'
ZIP = 'zip'
DIST = 'dist'
END = 'end'
DEBUG = False

def decimal_to_dms(decimal_deg, is_lat = True):
    '''
    @requires: decimal_deg - str
                is_lat - boolen
    @modifies: None
    @effects: None
    @raises: None
    @returns: str dms 
    '''
    negative = decimal_deg < 0
    dd = abs(decimal_deg)
    degrees = int(dd)
    minutes_float = (dd - degrees) * 60
    minutes = int(minutes_float)
    seconds = round((minutes_float - minutes) * 60, 2)
    
    if negative:
        direction = 'S' if is_lat else 'W'
    else:
        direction = 'N' if is_lat else 'E'
    
    deg_str = f"{degrees:03d}"
    min_str = f"{minutes:02d}"
    sec_str = f"{seconds:05.2f}"
    
    return f"({deg_str}°{min_str} {sec_str}\"{direction})"

def zip_to_dict():
    '''
    @requires: from zip_util import read_zip_all
    @modifies: None
    @effects: None
    @raises: None
    @returns: zip_to_dict - dict of dicts {zip_code:{zip_code,lat,lon,city,state,country}}
            zip_code, city, state, contry - str
            lat,lon - float
    '''
    zip_codes = read_zip_all()
    zip_to_dict = {}
    city_state_to_zips = {}
    for row in zip_codes:
        if len(row) >= 6:
            zip_code = row[0].strip()
            lat = row[1]
            lon = row[2]
            city = row[3].strip().lower()
            state = row[4].strip().lower()
            country = row[5].strip().lower()
            
            info = {
                'zip_code': zip_code,
                'lat': lat,
                'lon': lon,
                'lat_str': decimal_to_dms(lat, True),
                'lon_str': decimal_to_dms(lon, False),
                'city': city,
                'state': state,
                'country': country
                } 
            zip_to_dict[zip_code] = info
           
            key = (city, state)
            if key not in city_state_to_zips:
                city_state_to_zips[key] = []
            city_state_to_zips[key].append(zip_code)
    
    return zip_to_dict, city_state_to_zips

def read_command():
    '''
    @requires: None
    @modifies: None
    @effects: None
    @raises: invalid str -> else
    @returns: command - str , default command = 'end'
    '''    
    command = END
    while True:
        user_answer = input("Command ('loc', 'zip', 'dist', 'end') => ").strip().lower()
        if user_answer == LOC:
            command = LOC
            break
        elif user_answer == ZIP:
            command = ZIP
            break
        elif user_answer == DIST:
            command = DIST
            break
        elif user_answer == END:
            command = END
            break
        else:
            print('Invalid command, ignoring')
            
    return command

def loc_command(data):
    '''
    @requires: data - dict of dicts {zip_code:{zip_code,lat,lon,city,state,country}}
            zip_code, city, state, contry, lat_str, lon_str - str
            lat,lon - floats
    @modifies: None
    @effects: None
    @raises: invalid key -> except KeyError
    @returns: None
    '''
    while True:
        user_answer = input('Enter a ZIP Code to lookup => ').strip()
        print(user_answer)
        try:
            lookup = data[user_answer]
            print(f"ZIP Code {lookup['zip_code']} is in {lookup['city']}, {lookup['state']}, {lookup['country']}")
            print(f"coordinates : {lookup['lat_str']}, {lookup['lon_str']}")
            break
        except KeyError:
            print(f"Key {user_answer} not found in dictionary")        

def zip_command(data):
    '''
    @requires: data - dict of lists {('city', 'state':[zip_code])}
            zip_code, city, state, contry - str
    @modifies: None
    @effects: None
    @raises: invalid key -> if not zips
    @returns: None
    '''
    while True:
        city = input('Enter a city name to lookup => ').strip().lower()
        print(city)
        state = input('Enter the state name to lookup => ').strip().lower()
        print(state)
        key = (city, state)
        zips = data.get(key)
        city_t, state_t = city.title(), state.title()
        if not zips:
            print(f"No ZIP Code(s) found for {city_t}, {state_t}")
        else:
            print(f"The following ZIP Code(s) found for {city_t}, {state_t}: " + ", ".join(zips))
            break

def haversine(lat1, lon1, lat2, lon2):
    '''
    @requires: lat1, lon1 - float - latitude / longitude of first GPS point (degrees),
                lat2, lon2 - float - latitude / longitude of second GPS point (degrees)
    @modifies: None
    @effects: None
    @raises: None
    @returns: dist_miles - float - distance in miles between 2 GPS points
    '''
    R = 6371.0
    km_to_miles = 0.621371
    
    lat1_rad = math.radians(lat1)    
    lon1_rad = math.radians(lon1)    
    lat2_rad = math.radians(lat2)    
    lon2_rad = math.radians(lon2) 
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = (math.sin(dlat / 2) ** 2 + 
         math.cos(lat1_rad)* math.cos(lat2_rad)* math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dist_miles = R * c * km_to_miles
    
    return dist_miles
    
def dist_command(data):
    '''
    @requires: data - dict of dicts {zip_code:{zip_code,lat,lon,city,state,country}}
            zip_code, city, state, contry, lan_str, lon_str - str
            lat,lon - floats
    @modifies: None
    @effects: None
    @raises: invalid key -> except KeyError
    @returns: None
    '''
    while True:
        zip_1 = input('Enter the first ZIP Code => ')
        print(zip_1)
        zip_2 = input('Enter the second ZIP Code => ')
        print(zip_2)
        try:
            lookup_1 = data[zip_1]
            lookup_2 = data[zip_2]
            lat1 = lookup_1['lat']
            lon1 = lookup_1['lon']
            lat2 = lookup_2['lat']
            lon2 = lookup_2['lon']
            
            dist = haversine(lat1, lon1, lat2, lon2)
            print(f"The distance berween {zip_1} and {zip_2} is {dist:.2f} miles")
            break
            
        except KeyError as e:
            print(f"Key {e} not found in dictionary")           
        
    
zip_to_dict, city_state_to_zips = zip_to_dict()

if not DEBUG:
        
    while True:
        command = read_command()
        print(command)
        if command == END:
            print('Done')
            break
        elif command == LOC:
            loc_command(zip_to_dict)
        elif command == ZIP:
            zip_command(city_state_to_zips)
        elif command == DIST:
            dist_command(zip_to_dict)
    
    print('Finished')
        
else:  
    '''
    test-cases
    '''
    #decimal_to_dms
    expected = '(042°40 25.32"N), (073°36 31.65"W)'
    actual_lat = decimal_to_dms(42.673701, True)
    actual_lon =_lon = decimal_to_dms(-73.608792, False)
    if expected != actual_lat + ', ' + actual_lon:
        print('Test decimal_to_dms 1 failed')
    
    #zip_to_dict
    expected = dict
    actual = type(zip_to_dict)
    if expected != actual:
        print('Test zip_to_dict 1 failed')
    
    expected = 42049
    actual =  len(zip_to_dict)
    if expected != actual:
        print('Test zip_to_dict 2 failed')
        
    expected = 8
    actual = len(zip_to_dict['00601'])
    if expected != actual:
        print('Test zip_to_dict 3 failed')
    #haversine
    expected = 201.85669141508222
    actual = haversine(42.673701, -73.608792, 40.191907, -75.66531)
    if expected != actual:
        print('Test haversine 1 failed')
        

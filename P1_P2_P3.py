#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 21:07:31 2025

@author: nadya_urba
"""

import math
FEET_PER_YARD = 3
FEET_PER_MILE = 5280
SEC_PER_HOUR = 3600


def input_data():
    '''
    @requires: None
    @modifies: None
    @effects: None
    @raises: None       
    @returns: 
        data : type dict
    '''
    data = {}
    questions = [('d1', 'Введите кратчайшее расстояние между спасателем и кромкой воды, d1 (ярды): '),
                 ('d2', 'Введимите кратчайшее расстояние от утопающего до берега, d2 (футы): '),
                 ('h', 'Введите боковое смещение между спасателем и утопающим, h (ярды): '),
                 ('v_sand', 'Введите скорость движения спасателя по песку, v_sand (мили в час): '),
                 ('n', 'Введите коэффициент замедления спасателя при движении в воде, n: '),
                 ('theta1', 'Введите коэффициент замедления спасателя по песку, theta1 (градусы): ')]
    for key, question in questions:
        data[key] = float(input(question))
    
    return data    
    
    
def calculations(data):
    '''
    @requires:
        data : type dict
            keys : d1, d2, h, v_sand, n, theta1
            values : type float
    @modifies: None
    @effects: None
    @raises: None       
    @returns: 
        t : type float
    '''
    d1 = data['d1'] * FEET_PER_YARD
    d2 = data['d2']
    h = data['h'] * FEET_PER_YARD
    v_sand = data['v_sand'] * FEET_PER_MILE 
    n = data['n']
    theta1 = math.radians(data['theta1'])
     
    x = d1 * math.tan(theta1)
    L1 = math.sqrt(math.pow(x, 2) + math.pow(d1, 2))
    L2 = math.sqrt(math.pow((h- x), 2) + math.pow(d2, 2))            
    t = ((L1 + n * L2) / v_sand) * SEC_PER_HOUR
    return t
    
def output_data(result, theta1):
    '''
    @requires:
        result : type float
        theta1 : type str
    @modifies: None
    @effects: None
    @raises: None       
    @returns: None
    '''
    result = (f"{result:.1f}")
    print('Если спасатель начнет движение под углом theta1, равным ', theta1, 'градусам, он достигнет утопающего через ', result, ' секунды')

def optimal_angle(data):
    '''
    @requires:
        data : type dict
            keys : d1, d2, h, v_sand, n, theta1
            values : type float
    @modifies: None
    @effects: None
    @raises: None       
    @returns: 
        t : type float
    '''
    min_time = 999999
    best_theta = 0
    for theta in range(0, 90,  1):
        new_data = data.copy()
        new_data['theta1'] = theta
        t = calculations(new_data)
        if t < min_time:
            min_time = t
            best_theta = theta
    print(f"Оптимальный угол: {best_theta}° (время: {min_time:.1f}с)")

'''
Check
'''
#user_data = input_data()
#result = calculations(user_data)
#output_data(result, user_data['theta1'])
#optimal_angle(user_data)

'''
test-cases
'''
total = 0
passed = 0

#test №1 Reference values
total +=1
data_set = {('d1', 8), ('d2', 10), ('h', 50), ('v_sand', 5), ('n', 2), ('theta1', 39.413)}
data = dict(data_set)
expected = 39.9  
result_1 = calculations(data)
result = (f"{result_1:.1f}")

if expected == float(result):
    passed += 1
    print('Test №', total, ' completed successfully.')
else:
    print('Test № ', total, 'failed.')
    
#test №2 Check for negative values
total +=1
bad_value = 0
user_data = input_data()
for i in user_data:
    value = user_data[i]
    if value < 0:
        print('Значение', i, value, '- отрицательное')
        bad_value =+1
if bad_value == 0:
    passed +=1
    print('Test №', total, ' completed successfully.')
else:
    print('Test № ', total, 'failed.')

#test № 3 Check for zero values
total +=1
bad_value = 0
user_data = input_data()
for i in user_data:
    value = user_data[i]
    if value == 0:
        print('Значение', i, value, '- равно нулю')
        bad_value =+1
if bad_value == 0:
    passed +=1
    print('Test №', total, ' completed successfully.')
else:
    print('Test № ', total, 'failed.')


print('Всего тестов: ', total)
print('Успешно пройдено: ', passed)

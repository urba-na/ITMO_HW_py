#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 15:16:58 2026

@author: nadya_urba
"""
import FM_model_db as model
import FM_view as view
import math

R = 3958.8

'''
Возвращает общее количество рынков в БД
'''
def total_count():
    return model.total_count()[0]

'''
Выводит заголовки и форматированный список рынков.    
    Args:
        markets_data - cписок кортежей (fmid, name, country, state, city, rating)
'''
def processing_list(markets_data):
    view.print_headlines()
    for row in markets_data:
        fmid, name, country, state, city, rating = row
        name = name[:34]
        city = city[:19]
        rating_str = f"{float(rating):5.1f}*"
        view.print_list(fmid, name, country, state, city, rating_str)

'''
Отображает список рынков.
    Args:
        page (int) - номер страницы (начиная с 0)
        page_size (int) - количество рынков на странице
'''    
def display_list(page, page_size):
    offset = page * page_size
    markets_data = model.markets_list(page_size, offset)
    processing_list(markets_data)
    
'''
Отображает отфильтрованный список рынков по городу и штату.
    Args:
        city (str) - название города
        state (str) - название штата
'''    
def filtered_list(city, state):
    markets_data = model.filtered_list(city, state)
    processing_list(markets_data)

'''
Отображает детальную информацию о рынке и его отзывы. 
    Args:
        fmid (int) - ID рынка    
    Returns:
        None -  выводит детали или сообщение "не найдено"
'''    
def market_details(fmid):
    market = model.get_market_details(fmid)
    avg_rating = model.get_average_rating(fmid)
    reviews = model.get_market_reviews(fmid)
    if not market:
        view.print_not_found()
        return   
    view.print_details(market, avg_rating, reviews)

'''
Вычисляет расстояние между двумя точками на Земле по формуле Haversine.
    Args:
        lat1, lon1 (float) - координаты первой точки (широта, долгота)
        lat2, lon2 (float) - координаты второй точки (широта, долгота)
    Returns:
        float - расстояние в милях
'''      
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))
 
'''
Находит рынки в радиусе от заданного почтового индекса.    
    Args:
        zip_code (str) - почтовый индекс центра
        miles (str) - радиус поиска в милях
    Returns:
        list - список отфильтрованных рынков с расстояниями или []
'''       
def get_zip_radius(zip_code, miles):
    miles_float = float(miles)
    markets = model.get_markets_zip_radius()
    center = model.get_zip_center(zip_code) 
    
    if not center: 
        view.print_not_found()
        return []
    
    lat_c, lon_c = float(center[0]), float(center[1])
    filtered = []
    
    for market in markets:
        x = float(market[6]) if market[6] else None
        y = float(market[7]) if market[7] else None 
        
        if x and y:
            distance = haversine(lat_c, lon_c, x, y)
            if distance <= miles_float:
                filtered.append((market, distance))
    if filtered:
        view.print_zip_markets(filtered, miles, zip_code, lat_c, lon_c, market, distance)        
    else:
        view.print_not_found()

'''
Добавляет новый отзыв к рынку.
    Args:
        fmid (int) - ID рынка
        name (str) - имя автора отзыва
        rating (float) - оценка (1-5)
        text (str) - текст отзыва
'''
def add_review(fmid, name, rating, text):
    answer = model.add_review(fmid, name, rating, text)
    if answer:
        view.print_success()
  
'''
Отображает топ-N рынков, отсортированных по рейтингу. 
    Args:
        count (int) - количество рынков для вывода
'''        
def sort_by_rating(count):
    markets_data = model.filtered_list(limit = count)
    processing_list(markets_data)

'''
Удаляет рынок из базы данных.
    Args:
        fmid (int) - ID рынка для удаления
'''
def delete_market(fmid):
    answer = model.delete_market(fmid)
    if answer:
        view.print_deleted()
        
if __name__ == '__main__':
    print()
    

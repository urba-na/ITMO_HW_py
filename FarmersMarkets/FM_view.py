#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 14:56:07 2026

@author: nadya_urba
"""

def prompt_help():
    print("\n Для описания команд help")

def print_prompt():
    print("\n Commands : list, next, prev, city, details, zip, sort, review, delete, quit")
    
def print_help():
    print("\n=== КОМАНДЫ ===")
    print("list     - показать текущую страницу рынков")
    print("next     - следующая страница")
    print("prev     - предыдущая страница") 
    print("city     - поиск по городу и штату")
    print("details  - подробности рынка")
    print("zip      - поиск рынков в радиусе от ZIP")
    print("sort     - сортировка по рейтингу (по убыванию)")
    print("review   - добавить отзыв")
    print("delete   - удалить рынок")
    print("quit     - выход")

def print_command(command):
    print(command)
    
def print_headlines():
    print(f"{'FMID':<10} {'MarketName':<35} {'City':<20} {'State':<12} {'Rating':<8}")
    print("-" * 90)
    
def print_list(fmid, name, country, state, city, rating_str):
    print(f"{fmid:<10} {name:<35} {city:<20} {state:<12} {rating_str:<6}")

def print_pages(current_page, total_pages):
    print(f"\nСтраница {current_page + 1} из {total_pages}")
    
def print_warning(current_page, total_pages):
    if current_page < 0:
        print('!!! Команда prev не может быть выполнена, тк вы находитесь на 1 странице')
    elif current_page >= total_pages:
         print('!!! Комаеда next  не может быть выполнена, тк вы нахрлитесь на последней странице')
         
def print_intro_city():
    print('Введите название города и/или штата')

def print_intro_zip():
    print('Введите индекс и расстояние поиска в милях')
    
def print_intro_det():
    print('Введите fmid рынка')
    
def print_not_found():
    print('Рынок не найден')
    
def print_details(market, avg_rating, reviews):
    print(f"\n{'='*60}")
    print(f"{market[1].upper()}")
    print(f"{'='*60}")
    print(f"Адрес: {market[2] if market[2] else 'N/A'}, {market[3] if market[3] else 'N/A'}")
    print(f"{market[4] if market[4] else 'N/A'} | ZIP: {market[5] if market[5] else 'N/A'}")
    print(f"Координаты: {market[6] if market[6] else 'N/A'}/{market[7] if market[7] else 'N/A'}")
    print(f"Рейтинг: {float(avg_rating):.1f} ({len(reviews)} отзывов)")
    if reviews:
        print("\nОтзывы:")
        for i, review in enumerate(reviews, 1):
            if isinstance(review, tuple):
                name, rating, text, date = review
                print(f"{i}. {name} ({rating}): {text}")
                print(f"   {date.strftime('%d.%m.%Y %H:%M')}")
            else:
                print(f"{i}. {review}")
    else:
        print("Отзывов пока нет")
            
def print_zip_markets(filtered, miles, zip_code, lat_c, lon_c,market, distance):
    print(f"\n{len(filtered)} РЫНКОВ в радиусе {miles} миль от ZIP {zip_code}")
    print(f"Центр: {lat_c:.4f}°, {lon_c:.4f}°")
    print("=" * 90)
    print(f"{'#':<3} {'FMID':<10} {'НАЗВАНИЕ':<35} {'ГОРОД':<12} {'РАССТОЯНИЕ'}")
    print("-" * 90)
    for i, (market, distance) in enumerate(filtered, 1):
        city = market[3] if market[3] else "N/A"
        print(f"{i:<3} {market[0]:<10} {market[1][:34]:<35} {city:<12} {distance:6.2f}м")
        
    print("=" * 90)
    
def print_required_field():
    print('Это обязательное для заполнения поле')
    
def print_intro_review():
    print('Введите fmid, имя, оценку и отзыв')
    
def print_raiting_warning():
    print("Рейтинг должен быть от 1 до 5")
    
def print_raiting_warning_int():
    print("Рейтинг должен быть числом")
    
def print_success():
    print('Операция выполнена успешно')
    
def print_cancl():
    print('Операция отменена')   

def print_intro_del():
    print('Удаление данных из базы возможно только для пользователей с правами администратора')
    print('Введите fmid рынка')

def print_invalid_command():
    print("Неверная команда, игнорировать")
    
def print_newline():
    print()
    
def print_exit():
    print("Работа завершена")

def print_deleted():
    print('Рынок удален')
    
def print_ValueError():
    print('Введено неверное значение')
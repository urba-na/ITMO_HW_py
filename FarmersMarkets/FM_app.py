#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Created on Sat Feb 28 20:35:04 2026

@author: nadya_urba
"""

'''
Приложение читает данные из базы данных farmers_markets
    и позволяет выполнять следующие команды:
    > list        - показать текущую страницу рынков
    > next        - следующая страница  
    > prev        - предыдущая страница
    > city        - фильтр по городу+штату
    > zip         - поиск по ZIP + радиус
    > sort        - сортировка по рейтингу/популярности
    > details     - детали рынка по FMID
    > review      - оставить отзыв
    > delete      - удалить объект
    > quit        - выход;
    
команда delete работает только при запуске бд под test_adm - см model
'''

import FM_view as view
import FM_general as gen

PAGE_SIZE = 10
PAGES = gen.total_count()

def cmd_help():
    view.print_help()

def cmd_list(page):
    gen.display_list(page, PAGE_SIZE)
    view.print_pages(page, PAGES)
    
def cmd_next(page):
    if page >= PAGES:
        view.print_warning(page, PAGES)
        page = PAGES
    gen.display_list(page, PAGE_SIZE)
    view.print_pages(page, PAGES)

def cmd_prev(page):
    if page < 0:
        view.print_warning(page, PAGES)
        page = 0
    gen.display_list(page, PAGE_SIZE)
    view.print_pages(page, PAGES)

def cmd_city():
    view.print_intro_city()
    city = input('city: ').strip()
    state = input('state: ').strip()
    gen.filtered_list(city, state)
    
def cmd_det():
    view.print_intro_det()
    fmid = input('fmid: ').strip()
    gen.market_details(fmid)

def cmd_zip():
    view.print_intro_zip()
    while True:
        zip_code = input('ZIP: ').strip()
        if zip_code:
            break
        view.print_required_field()
    while True:
        miles = input('Мили: ').strip()
        if miles:
            break
        view.print_required_field()
        
    gen.get_zip_radius(zip_code, miles)

def cmd_sort():
    count = int(input('Вывести по убыванию рейтинга первые: '))
    gen.sort_by_rating(count)

def cmd_review():
    view.print_intro_review()
    while True:
        fmid = input('FMID: ').strip()
        if fmid:
            break
        view.print_required_field()
    
    while True:
        name = input('Имя: ').strip()
        if name:
            break
        view.print_required_field()
    
    while True:
        rating = input('Рейтинг (1-5): ').strip()
        try:
            rating_int = int(rating)
            if 1 <= rating_int <= 5:
                break
            view.print_raiting_warning()
        except ValueError:
            view.print_raiting_warning_int()
    
    text = input('Комментарий (необязательно): ').strip()
    gen.add_review(fmid, name, rating, text)

def cmd_del():
    view.дшые()
    fmid = input('fmid: ');
    confirm = input("УДАЛИТЬ? (да/нет): ").strip().lower()
    if confirm in ['да']:
        gen.delete_market(fmid)
    else:
        view.print_cancl()

page = 0
command = ""
view.prompt_help()

while command != 'quit':
    view.print_prompt()
    command = input("\n> ")
    command = command.strip().lower()
    if command == 'help':
        cmd_help()
    elif command == 'list':
        cmd_list(page)
    elif command == 'next':
        page += 1
        cmd_next(page)
    elif command == 'prev':
        page -= 1
        cmd_prev(page)
    elif command == 'city':
        cmd_city()
    elif command == 'details':
        cmd_det()
    elif command == 'zip':
        cmd_zip()
    elif command == 'sort':
        cmd_sort()
    elif command == 'review':
        cmd_review()
    elif command == 'delete':
        cmd_del()
    elif command != 'quit':
        view.print_invalid_command()
    view.print_newline()
view.print_exit()

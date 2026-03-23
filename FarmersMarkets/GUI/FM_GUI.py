#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 21:04:55 2026

@author: nadya_urba
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import FM_model_db as model
import FM_general as gen

PAGE_SIZE = 10

class FarmersMarketGUI:
    '''
    @requires: root — объект Tk/Tkinter (root = tk.Tk())
    @modifies: self.root, self.page, self.selected_fmid, создает виджеты (notebook, info_label, tree, details_text)
    @effects: создает главное окно GUI, настраивает окно (title, geometry), привязывает WM_DELETE_WINDOW к on_closing,
              вызывает setup_ui(), update_total_pages(), refresh_list()
    @returns: None
    '''    
    def __init__(self, root):
        self.root = root
        self.root.title("Фермерские рынки")
        self.root.geometry("1200x800")
        
        self.page = 0
        self.selected_fmid = None
  
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
           
        self.setup_ui()
        
        self.update_total_pages()
        self.refresh_list()
        
    '''
    @requires: None
    @modifies: закрывает курсор и соединение с БД (если открыты), уничтожает root-окно
    @effects:  закрывает соединение с БД FM_model_db и уничтожает главное окно
    @returns: None
    '''
    def on_closing(self):
        import FM_model_db
        try:
            FM_model_db.cur.close()
            FM_model_db.conn.close()
        except:
            pass
        self.root.destroy()
    
    '''
    @requires: self.root —  окно Tk; self.notebook будет создан как ttk.Notebook
    @modifies: self.notebook, создает и добавляет вкладки (main_frame, city_frame, zip_frame, review_frame)
    @effects: создает Notebook с несколькими вкладками и вызывает setup_main_tab(), setup_city_tab(),
              setup_zip_tab(), setup_review_tab()
    @returns: None
    '''
    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.setup_main_tab()
        self.setup_city_tab()
        self.setup_zip_tab()
        self.setup_review_tab()
    
    '''
    @requires: self.notebook —  ttk.Notebook
    @modifies: создается self.main_frame и виджеты на нём:
               btn_frame, кнопки Prev/List/Next/*Sort/Delete,
               self.tree (Treeview с колонками FMID, MarketName, City, State, Rating),
               self.details_text (ScrolledText)
    @effects: создает вкладку «Главная» с:
               - панелью кнопок,
               - таблицей рынков,
               - полем с деталями выбранного рынка
               привязывает события <<TreeviewSelect>> и <Double-1> к соответствующим методам
    @returns: None
    '''
    def setup_main_tab(self):
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="Главная")
        
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=(0,10))
        
        ttk.Button(btn_frame, text="Prev", command=self.cmd_prev).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="List", command=self.cmd_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Next", command=self.cmd_next).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="* Sort", command=self.cmd_sort).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.cmd_delete).pack(side=tk.LEFT, padx=5)
        
        self.info_label = ttk.Label(self.main_frame, text="Загрузка...")
        self.info_label.pack(pady=(0,5))
        
        tree_frame = ttk.LabelFrame(self.main_frame, text="Рынки (двойной клик = детали)")
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0,5))
        
        columns = ("FMID", "MarketName", "City", "State", "Rating")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.tree.bind('<Double-1>', self.on_market_double_click)
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        
        details_frame = ttk.LabelFrame(self.main_frame, text="Детали выбранного рынка")
        details_frame.pack(fill=tk.BOTH, expand=True)
        self.details_text = scrolledtext.ScrolledText(details_frame, height=10, font=("Courier", 9))
        self.details_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    '''
    @requires: self.notebook —  ttk.Notebook
    @modifies: создается self.main_frame и виджеты на нём:
               btn_frame, кнопки Prev/List/Next/*Sort/Delete,
               self.tree (Treeview с колонками FMID, MarketName, City, State, Rating),
               self.details_text (ScrolledText)
    @effects: создает вкладку «Главная» с:
               - панелью кнопок,
               - таблицей рынков,
               - полем с деталями выбранного рынка
               привязывает события <<TreeviewSelect>> и <Double-1> к соответствующим методам
    @returns: None
    '''
    def setup_city_tab(self):
        city_frame = ttk.Frame(self.notebook)
        self.notebook.add(city_frame, text="City")
        
        ttk.Label(city_frame, text="Поиск по городу / штату", font=('Arial', 14, 'bold')).pack(pady=20)
        
        form_frame = ttk.LabelFrame(city_frame, text="Данные")
        form_frame.pack(fill=tk.X, padx=50, pady=20)
        
        ttk.Label(form_frame, text="City:").grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.city_entry = ttk.Entry(form_frame, width=30)
        self.city_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(form_frame, text="State:").grid(row=1, column=0, sticky='w', padx=10, pady=10)
        self.state_entry = ttk.Entry(form_frame, width=30)
        self.state_entry.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Button(form_frame, text="Найти", command=self.cmd_city_search).grid(row=2, column=0, columnspan=2, pady=20)
        
        self.city_result = scrolledtext.ScrolledText(city_frame, height=20, font=("Courier", 10))
        self.city_result.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
    
    '''
    @requires: self.notebook —  ttk.Notebook
    @modifies: создается zip_frame и элементы:
               self.zip_entry, self.miles_entry, self.zip_result (ScrolledText),
               при создании вставляются значения по умолчанию: ZIP='19565', Мили='6000'
    @effects: создает вкладку «ZIP» с полями ввода ZIP и миль, кнопкой «Найти»,
              привязанной к cmd_zip_search(), и областью вывода результатов
    @returns: None
    '''
    def setup_zip_tab(self):
        zip_frame = ttk.Frame(self.notebook)
        self.notebook.add(zip_frame, text="ZIP")
        
        ttk.Label(zip_frame, text="Поиск по ZIP + расстоянию в милях", font=('Arial', 14, 'bold')).pack(pady=20)
        
        form_frame = ttk.LabelFrame(zip_frame, text="Данные")
        form_frame.pack(fill=tk.X, padx=50, pady=20)
        
        ttk.Label(form_frame, text="ZIP:").grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.zip_entry = ttk.Entry(form_frame, width=20)
        self.zip_entry.grid(row=0, column=1, sticky='w', padx=10, pady=10)
        self.zip_entry.insert(0, "19565")
        
        ttk.Label(form_frame, text="Мили:").grid(row=1, column=0, sticky='w', padx=10, pady=10)
        self.miles_entry = ttk.Entry(form_frame, width=20)
        self.miles_entry.grid(row=1, column=1, sticky='w', padx=10, pady=10)
        self.miles_entry.insert(0, "6000")
        
        ttk.Button(form_frame, text="Найти", command=self.cmd_zip_search).grid(row=2, column=0, columnspan=2, pady=20)
        
        self.zip_result = scrolledtext.ScrolledText(zip_frame, height=25, font=("Courier", 10))
        self.zip_result.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
    
    '''
    @requires: self.notebook —  ttk.Notebook
    @modifies: создается review_frame и элементы:
               self.review_fmid_entry, self.review_name_entry, self.review_text,
               self.review_rating_var + self.review_rating_combo (выбор 1–5),
               self.review_status (Label)
    @effects: создает вкладку «Review» с формой добавления отзыва:
               - FMID, имя, рейтинг (1–5), комментарий,
               - кнопкой «Сохранить» (cmd_save_review),
               - статус‑лейблом для результата сохранения
    @returns: None
    '''
    def setup_review_tab(self):
        review_frame = ttk.Frame(self.notebook)
        self.notebook.add(review_frame, text="Review")
        
        ttk.Label(review_frame, text="Добавить отзыв", font=('Arial', 14, 'bold')).pack(pady=20)
        
        form_frame = ttk.LabelFrame(review_frame, text="Данные")
        form_frame.pack(fill=tk.X, padx=50, pady=20)
        
        ttk.Label(form_frame, text="FMID:").grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.review_fmid_entry = ttk.Entry(form_frame, width=15)
        self.review_fmid_entry.grid(row=0, column=1, sticky='w', padx=10, pady=10)
        
        ttk.Label(form_frame, text="Имя:").grid(row=1, column=0, sticky='w', padx=10, pady=10)
        self.review_name_entry = ttk.Entry(form_frame, width=30)
        self.review_name_entry.grid(row=1, column=1, sticky='w', padx=10, pady=10)
        
        ttk.Label(form_frame, text="Рейтинг:").grid(row=2, column=0, sticky='w', padx=10, pady=10)
        self.review_rating_var = tk.StringVar(value="5")
        self.review_rating_combo = ttk.Combobox(form_frame, textvariable=self.review_rating_var, values=[1,2,3,4,5], width=27)
        self.review_rating_combo.grid(row=2, column=1, sticky='w', padx=10, pady=10)
        
        ttk.Label(form_frame, text="Комментарий:").grid(row=3, column=0, sticky='nw', padx=10, pady=10)
        self.review_text = tk.Text(form_frame, height=6, width=40)
        self.review_text.grid(row=3, column=1, sticky='w', padx=10, pady=10)
        
        ttk.Button(form_frame, text="Сохранить", command=self.cmd_save_review).grid(row=4, column=0, columnspan=2, pady=20)
        
        self.review_status = ttk.Label(review_frame, text="Статус: Готов", font=('Arial', 12))
        self.review_status.pack(pady=10)
        
    '''
    @requires: model.total_count() —  функция, возвращающая кортеж/список с одним числом (общее количество рынков)
    @modifies: self.total_count, self.total_pages
    @effects: обновляет общее количество рынков и вычисляет общее число страниц
    @returns: None
    '''
    def update_total_pages(self):
        self.total_count = model.total_count()[0]
        self.total_pages = (self.total_count + PAGE_SIZE - 1) // PAGE_SIZE
    
    '''
    @requires: self.tree —  ttk.Treeview с колонками FMID, MarketName, City, State, Rating;
               model.markets_list(limit, offset) —  функция, возвращающая список рынков
    @modifies: очищает self.tree, обновляет содержимое таблицы рынков и self.info_label
    @effects: заполняет таблицу markets (PAGE_SIZE строк) с текущей страницы,
              обновляет метку с текущей страницей и общим количеством рынков;
              при ошибке показывает текст ошибки в info_label
    @returns: None
    '''
    def refresh_list(self):
        self.tree.delete(*self.tree.get_children())
        
        try:
            markets = model.markets_list(PAGE_SIZE, self.page * PAGE_SIZE)
            for row in markets:
                fmid, name, country, state, city, rating = row
                self.tree.insert("", "end", values=(fmid, name[:35], city, state, f"{float(rating):.1f}"))
            
            self.update_total_pages()
            self.info_label.config(text=f"{self.page+1}/{self.total_pages} | Рынков: {self.total_count}")
        except Exception as e:
            self.info_label.config(text=f"Ошибка загрузки: {e}")

    '''
    @requires: self.tree —  Treeview с привязанным <<TreeviewSelect>>;
               self.selected_fmid — внутреннее состояние класса
    @modifies: self.selected_fmid, self.info_label
    @effects: при выделении строки в таблице устанавливает self.selected_fmid в значение FMID выбранного рынка
              и обновляет текст info_label
    @returns: None
    '''
    def on_tree_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.selected_fmid = item['values'][0]
            self.info_label.config(text=f"{self.page+1}/{self.total_pages} | Выбран FMID={self.selected_fmid}")
    
    '''
    @requires: self.selected_fmid —  установлен на число/строку FMID (через on_tree_select);
               привязано событие <Double-1> к self.tree
    @modifies: None
    @effects: при двойном клике по строке таблицы вызывает cmd_details() для отображения деталей рынка
    @returns: None
    '''
    def on_market_double_click(self, event):
        if self.selected_fmid:
            self.cmd_details()
 
    '''
    @requires: self.page — текущий номер страницы;
               вызов refresh_list()
    @modifies: self.page = 0, обновляет self.tree через refresh_list()
    @effects: переходит к первой странице списка рынков и обновляет таблицу
    @returns: None
    '''
    def cmd_list(self):
        self.page = 0
        self.refresh_list()
        
    '''
    @requires: вызов update_total_pages() для актуального значения self.total_pages;
               self.page < self.total_pages
    @modifies: self.page (увеличивает на 1, если возможно), self.tree и self.info_label через refresh_list()
    @effects: переходит к следующей странице списка рынков;
              если текущая страница последняя, выводит в info_label «Последняя страница!»
    @returns: None
    '''
    def cmd_next(self):
        self.update_total_pages()
        if self.page < self.total_pages - 1:
            self.page += 1
            self.refresh_list()
        else:
            self.info_label.config(text="Последняя страница!")
   
    '''
    @requires: вызов update_total_pages() для актуального значения self.total_pages;
               self.page >= 0
    @modifies: self.page (уменьшает на 1, если возможно), self.tree и self.info_label через refresh_list()
    @effects: переходит к предыдущей странице списка рынков;
              если текущая страница первая, выводит в info_label «Первая страница!»
    @returns: None
    '''
    def cmd_prev(self):
        self.update_total_pages()
        if self.page > 0:
            self.page -= 1
            self.refresh_list()
        else:
            self.info_label.config(text="Первая страница!")
    
    '''
    @requires: model.filtered_list(limit=30) —  функция, возвращающая отсортированный список рынков (по рейтингу);
               self.tree —  Treeview с колонками FMID, MarketName, City, State, Rating
    @modifies: очищает self.tree, заполняет его TOP‑30 рынков, обновляет self.info_label
    @effects: показывает в таблице 30 лучших рынков по рейтингу с пометкой «*» у рейтинга;
              обновляет текст info_label на «ТОП-30 рынков по рейтингу»
    @returns: None
    '''
    def cmd_sort(self):
        count = 30
        self.tree.delete(*self.tree.get_children())
        markets_data = model.filtered_list(limit=count)
        
        for row in markets_data:
            fmid, name, country, state, city, rating = row
            name = name[:34]
            self.tree.insert("", "end", values=(fmid, name, city[:19], state, f"{float(rating):.1f}*"))
        
        self.info_label.config(text=f"ТОП-{count} рынков по рейтингу")

    '''
    @requires: self.selected_fmid — установлен (не None); self.details_text — ScrolledText;
               model.get_market_details(fmid), model.get_average_rating(fmid), model.get_market_reviews(fmid) —
                функции доступа к БД
    @modifies: self.details_text (полностью очищает и заполняет деталями рынка и отзывов)
    @effects: выводит в деталях:
               - инфо рынка (FMID, MarketName, адрес, ZIP, координаты, товары, услуги),
               - средний рейтинг и число отзывов,
               - до 3 последних отзывов (если есть);
               при отсутствии рынка или ошибке показывает сообщение об ошибке
    @returns: None
    '''
    def cmd_details(self):
        if not self.selected_fmid:
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, "Сначала выбери рынок кликом!")
            return
     
        fmid_str = str(self.selected_fmid) 
        
        self.details_text.delete(1.0, tk.END)
        
        try:
            market = model.get_market_details(fmid_str)
            avg_rating = model.get_average_rating(fmid_str)
            reviews = model.get_market_reviews(fmid_str)
            
            if market:
                output = f"{'='*70}\n{market[1].upper()}\n{'='*70}\n"
                output += f"FMID: {market[0]}\n"
                output += f"Адрес: {market[2] or 'N/A'}\n"
                output += f"Город/округ: {market[3] or 'N/A'}\n"
                output += f"ZIP: {market[4] or 'N/A'}\n"
                output += f"Координаты: {market[5] or 'N/A'}, {market[6] or 'N/A'}\n"
                output += f"Обновлено: {market[7] or 'N/A'}\n"
                output += f"Товары: {market[8] or 'нет данных'}\n"
                output += f"Услуги: {market[9] or 'нет данных'}\n"
                output += f"Рейтинг: {float(avg_rating):.1f}★ ({len(reviews)} отзывов)\n"
                
                if reviews:
                    output += f"\nПоследние отзывы:\n"
                    for i, review in enumerate(reviews[:3], 1):
                        output += f"{i}. {review[0]} ({int(review[1])}★): {review[2][:80]}...\n"
                else:
                    output += "\nОтзывов пока нет\n"
                
                self.details_text.insert(tk.END, output)
            else:
                self.details_text.insert(tk.END, f"Рынок FMID={fmid_str} не найден в БД")
                
        except Exception as e:
            self.details_text.insert(tk.END, f"Ошибка загрузки деталей: {str(e)[:100]}")
            
    '''
    @requires: self.selected_fmid — может быть None или числом;
               gen.delete_market(fmid) — функция, логично удаляющая рынок из БД;
               model.get_market_details(fmid) —  функция для проверки существования рынка
    @modifies: состояние БД (удаление рынка), self.tree и info_label через refresh_list(),
               self.selected_fmid (устанавливает в None при успешном удалении)
    @effects: предупреждает пользователя через messagebox.askyesno, затем:
               - удаляет рынок по FMID,
               - при успехе обновляет список рынков и сбрасывает выбранный FMID;
               при ошибке/отказе показывает сообщение об ошибке или про неудалённый рынок
    @returns: None
    '''
    def cmd_delete(self):
        if not self.selected_fmid:
            fmid_input = simpledialog.askstring("Удаление", "Введите FMID:")
            if not fmid_input:
                return
            fmid = fmid_input.strip()
        else:
            fmid = str(self.selected_fmid)
        
        if messagebox.askyesno("УДАЛЕНИЕ", f"НАВСЕГДА удалить FMID={fmid}?"):
            try:
                success = gen.delete_market(fmid)
                if model.get_market_details(fmid) is None:
                    messagebox.showinfo("УСПЕХ", f"Рынок FMID={fmid} удален!")
                    self.refresh_list()
                    self.selected_fmid = None
                else:
                    messagebox.showerror("ОШИБКА", f"Рынок FMID={fmid} НЕ удален!")
                    
            except Exception as e:
                messagebox.showerror("ОШИБКА БД", f"Ошибка: {str(e)[:100]}")
        
    
    '''
    @requires: self.city_entry, self.state_entry, self.city_result —  виджеты;
               model.filtered_list(city, state) — функция фильтрации рынков по городу/штату
    @modifies: self.city_result (очищает и заполняет результатами поиска)
    @effects: выполняет поиск рынков по введённым_city и state,
              выводит в city_result количество найденных рынков и их данные в читаемом формате;
              если ничего не найдено, пишет «Не найдено»
    @returns: None
    '''
    def cmd_city_search(self):
        city = self.city_entry.get()
        state = self.state_entry.get()
        self.city_result.delete(1.0, tk.END)
        markets = model.filtered_list(city, state)
        if markets:
            self.city_result.insert(tk.END, f"Найдено {len(markets)} рынков:\n\n")
            for row in markets:
                self.city_result.insert(tk.END, f"{row[0]}: {row[1]} ({row[4]}, {row[3]}) - {row[5]}\n")
        else:
            self.city_result.insert(tk.END, "Не найдено")
    
    '''
    @requires: self.zip_entry, self.miles_entry, self.zip_result —  виджеты;
               model.get_zip_center(zip_code) — функция получения координат по ZIP;
               model.get_markets_zip_radius() — функция получения списка всех рынков с координатами;
               gen.haversine(lat1, lon1, lat2, lon2) — функция расчёта расстояния в милях
    @modifies: self.zip_result (очищает и заполняет рынками внутри радиуса)
    @effects: по введённому ZIP‑коду и милям:
               - находит центр (координаты),
               - фильтрует рынки по радиусу (haversine),
               - выводит отформатированный список FMID, названий, городов и расстояний;
               при отсутствии ZIP‑центра или ошибке показывает соответствующее сообщение
    @returns: None
    '''
    def cmd_zip_search(self):
        zip_code = self.zip_entry.get().strip()
        miles = self.miles_entry.get().strip()
        
        if not zip_code or not miles:
            self.zip_result.delete(1.0, tk.END)
            self.zip_result.insert(tk.END, "Заполните ZIP и Мили!")
            return
        
        self.zip_result.delete(1.0, tk.END)
        self.zip_result.insert(tk.END, f"Ищем рынки в радиусе {miles} миль от ZIP {zip_code}...\n\n")
        
        try:
            center = model.get_zip_center(zip_code)
            if not center:
                self.zip_result.insert(tk.END, "ZIP код не найден!")
                return
            
            lat_c, lon_c = float(center[1]), float(center[2])
            markets = model.get_markets_zip_radius()
            
            filtered = []
            for market in markets:
                x = float(market[6]) if market[6] else None
                y = float(market[7]) if market[7] else None
                if x and y:
                    distance = gen.haversine(lat_c, lon_c, x, y)
                    if distance <= float(miles):
                        filtered.append((market, distance))
            
            if filtered:
                self.zip_result.insert(tk.END, f"{len(filtered)} Рынков в радиусе {miles} миль:\n")
                self.zip_result.insert(tk.END, f"Центр: {lat_c:.4f}°, {lon_c:.4f}°\n\n")
                self.zip_result.insert(tk.END, f"{'#':<4} {'FMID':<10} {'НАЗВАНИЕ':<35} {'ГОРОД':<12} {'МИЛИ':<8}\n")
                self.zip_result.insert(tk.END, "-" * 70 + "\n")
                
                for i, (market, distance) in enumerate(filtered, 1):
                    city = market[3] if market[3] else "N/A"
                    self.zip_result.insert(tk.END, f"{i:<3} {market[0]:<10} {market[1][:34]:<35} {city:<12} {distance:6.1f}\n")
            else:
                self.zip_result.insert(tk.END, "Рынков в радиусе не найдено\n")
                
        except Exception as e:
            self.zip_result.insert(tk.END, f"Ошибка: {str(e)[:100]}\n")
    
    '''
    @requires: self.review_fmid_entry, self.review_name_entry, self.review_text, self.review_rating_var,
               self.review_status —  виджеты формы добавления отзыва;
               gen.add_review(fmid_int, name, rating_int, text) —  функция добавления отзыва в БД
    @modifies: состояние БД (добавление отзыва); self.review_status (статус‑текст);
               очищает поля формы (entry, text) и сбрасывает rating_var на "5"
    @effects: при корректных числовых FMID и рейтинге добавляет отзыв;
              при незаполненных полях или некорректных числах показывает соответствующий статус‑текст
    @returns: None
    '''
    def cmd_save_review(self):
        fmid = self.review_fmid_entry.get().strip()
        name = self.review_name_entry.get().strip()
        rating = self.review_rating_var.get()
        text = self.review_text.get(1.0, tk.END).strip()
        
        if not all([fmid, name, rating, text]):
            self.review_status.config(text="Заполните все поля!")
            return
        
        try:
            fmid_int = int(fmid)
            rating_int = int(rating)
            
            gen.add_review(fmid_int, name, rating_int, text)
            self.review_status.config(text="Отзыв добавлен в БД!")
            
            # очистка полей
            self.review_fmid_entry.delete(0, tk.END)
            self.review_name_entry.delete(0, tk.END)
            self.review_text.delete(1.0, tk.END)
            self.review_rating_var.set("5")
            
        except ValueError:
            self.review_status.config(text="FMID и Рейтинг должны быть числами!")
        except Exception as e:
            self.review_status.config(text=f"Ошибка: {str(e)[:50]}")
    
    
if __name__ == "__main__":
    import atexit
    
    def cleanup_db():
        try:
            import FM_model_db
            if hasattr(FM_model_db, 'cur'):
                FM_model_db.cur.close()
            if hasattr(FM_model_db, 'conn'):
                FM_model_db.conn.close()
            print("БД принудительно закрыто!")
        except:
            pass
    
    atexit.register(cleanup_db)
    
    root = tk.Tk()
    app = FarmersMarketGUI(root)
    root.mainloop()

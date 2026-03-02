#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 21:50:22 2026

@author: nadya_urba
"""

#!/usr/bin/env python3
import psycopg

conn = psycopg.connect(dbname="farmers_markets",
                       host="localhost",
                       user="test_user",
                       password="test123",
                       port="5432")
'''
conn = psycopg.connect(dbname="farmers_markets",
                       host="localhost",
                       user="test_adm",
                       password="test345",
                       port="5432")

'''
cur = conn.cursor()

def total_count():
    cur.execute("SELECT COUNT(*) FROM markets")
    return cur.fetchone()

def markets_list(limit, offset=0):
    """FMID, MarketName, Country, State, City, Rating"""
    cur.execute("""
        SELECT 
            m.FMID,
            m.MarketName,
            COALESCE(cn.CountryName, 'N/A') as CountryName,
            COALESCE(s.StateName, 'N/A') as StateName,
            COALESCE(ct.city, 'N/A') as CityName,
            COALESCE(AVG(r.Rating), 0)::numeric(3,1) as AvgRating
        FROM markets m
        LEFT JOIN addresses a ON m.FMID = a.FMID
        LEFT JOIN countries cn ON a.CountyID = cn.CountryID
        LEFT JOIN states s ON a.StateID = s.StateID
        LEFT JOIN cities ct ON a.CityID = ct.CityID
        LEFT JOIN reviews r ON m.FMID = r.FMID
        GROUP BY m.FMID, m.MarketName, cn.CountryName, s.StateName, ct.city
        ORDER BY m.MarketName
        LIMIT %s OFFSET %s
    """, (limit, offset))
    
    return cur.fetchall()

def filtered_list(city=None, state=None, limit=None, offset=0):
    query = """
        SELECT 
            m.FMID,
            m.MarketName,
            COALESCE(cn.CountryName, 'N/A') as CountryName,
            COALESCE(s.StateName, 'N/A') as StateName,
            COALESCE(ct.city, 'N/A') as CityName,
            COALESCE(AVG(r.Rating), 0)::numeric(3,1) as AvgRating
        FROM markets m
        LEFT JOIN addresses a ON m.FMID = a.FMID
        LEFT JOIN countries cn ON a.CountyID = cn.CountryID
        LEFT JOIN states s ON a.StateID = s.StateID
        LEFT JOIN cities ct ON a.CityID = ct.CityID
        LEFT JOIN reviews r ON m.FMID = r.FMID
        WHERE 1=1
        """
    params = []
    
    if city:
        query += " AND LOWER(ct.city) LIKE LOWER(%s)"
        params.append(f"%{city}%")
    if state:
        query += " AND LOWER(s.StateName) LIKE LOWER(%s)"
        params.append(f"%{state}%")
        
    query += """
        GROUP BY m.FMID, m.MarketName, cn.CountryName, s.StateName, ct.city
        ORDER BY COALESCE(AVG(r.Rating), 0) DESC NULLS LAST, m.MarketName ASC 
        LIMIT %s OFFSET %s
    """
    params.extend([limit, offset])
    
    cur.execute(query, params)
    return cur.fetchall()

def get_market_details(fmid):
    cur.execute("""
        SELECT 
            m.FMID,
            m.MarketName,
            a.street,
            COALESCE(ct.city, 'N/A') as city,
            COALESCE(s.StateName, 'N/A') as State,
            a.zip,
            a.x,
            a.y
        FROM markets m
        LEFT JOIN addresses a ON m.FMID = a.FMID
        LEFT JOIN states s ON a.StateID = s.StateID
        LEFT JOIN cities ct ON a.CityID = ct.CityID
        WHERE m.FMID = %s
    """, (fmid,))
    return cur.fetchone()

def get_average_rating(fmid):
    cur.execute("""
        SELECT COALESCE(AVG(r.Rating), 0)::numeric(3,1)
        FROM reviews r
        WHERE r.FMID = %s
    """, (fmid,))
    return cur.fetchone()[0]

def get_market_reviews(fmid, limit = 5):
    cur.execute("""
        SELECT 
            r.name,
            r.rating, 
            r.reviewtext, 
            r.createdat
        FROM reviews r
        WHERE r.FMID = %s
        ORDER BY r.createdat DESC
        LIMIT %s
    """, (fmid, limit))
    return cur.fetchall()

def get_markets_zip_radius(limit=100, offset=0):
    cur.execute("""
        SELECT 
            m.fmid,
            m.marketname,
            a.street,
            COALESCE(ct.city, 'N/A') as city,
            COALESCE(s.StateName, 'N/A') as State,
            a.zip,
            a.x,
            a.y
        FROM markets m
        LEFT JOIN addresses a ON m.fmid = a.fmid
        LEFT JOIN states s ON a.stateid = s.stateid
        LEFT JOIN cities ct ON a.cityid = ct.cityid
        WHERE a.x IS NOT NULL AND a.y IS NOT NULL
        ORDER BY m.marketname
        LIMIT %s OFFSET %s
    """, (limit, offset))
    return cur.fetchall()

def get_zip_center(zipcode):
    cur.execute("""
        SELECT x, y 
        FROM addresses 
        WHERE zip = %s AND x IS NOT NULL AND y IS NOT NULL
        LIMIT 1
    """, (zipcode,))
    return cur.fetchone()

def add_review(fmid, name, rating, text):
    try:
        cur.execute("""
            INSERT INTO reviews (fmid, name, rating, reviewtext) 
            VALUES (%s, %s, %s, %s)
            """, (fmid, name, rating, text))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Ошибка БД: {e}")
        return False
    
def delete_market(fmid):
    try:
        cur.execute("DELETE FROM market_services WHERE fmid = %s", (fmid,))
        
        cur.execute("DELETE FROM market_seasons WHERE fmid = %s", (fmid,))

        cur.execute("DELETE FROM market_products WHERE fmid = %s", (fmid,))

        cur.execute("DELETE FROM contacts WHERE fmid = %s", (fmid,))
        
        cur.execute("DELETE FROM reviews WHERE fmid = %s", (fmid,))
        
        cur.execute("DELETE FROM addresses WHERE fmid = %s", (fmid,))
        
        cur.execute("DELETE FROM markets WHERE fmid = %s", (fmid,))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Ошибка удаления: {e}")
        return False

if __name__ == '__main__':
    
    markets_data = markets_list(limit=5)
    print("FMID\tMarketName\t\tCity, State\tRating")
    print("-" * 60)
    for row in markets_data:
        fmid, name, country, state, city, rating = row
        name = name[:34]
        city = city[:19]
        rating_str = f"{float(rating):5.1f}*"
        
        print(f"{fmid:<10} {name:<35} {city:<20} {state:<12} {rating_str:<6}")
    cur.close()
    conn.close()
    

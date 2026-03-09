#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 18:55:52 2026

@author: nadya_urba
"""

"""
Модуль для генерации бесконечных последовательностей чисел.
Содержит итератор Fibo, генераторы integers и primes.
"""
import unittest

class Fibo:
    """
    Итератор, перечисляющий числа Фибоначчи: 0, 1, 1, 2, 3...
    
    @requires: None
    @modifies: self
    @effects: Генерирует следующее число Фибоначчи при каждом вызове __next__
    @raises: None
    @returns: Fibo объект (итерируемый)
    """
    def __init__(self):
        """
        @requires: None
        @modifies: self.a, self.b
        @effects: a=0, b=1
        @raises: None
        @returns: None
        """
        self.a = 0
        self.b = 1

    def __iter__(self):
        """
        @requires: None
        @modifies: None
        @effects: None
        @raises: None
        @returns: self (итератор)
        """
        return self

    def __next__(self):
        """
        @requires: None
        @modifies: self.a, self.b
        @effects: Обновляет до следующего числа
        @raises: None
        @returns: int — следующее число Фибоначчи
        """
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        return result


def integers():
    """
    Генератор всех неотрицательных целых чисел
    
    @requires: None
    @modifies: None
    @effects: Генерирует числа по возрастанию
    @raises: None
    @returns: generator — последовательность int начиная с 0
    """
    n = 0
    while True:
        yield n
        n += 1


def primes():
    """
    Генератор всех простых чисел
    
    @requires: None
    @modifies: None
    @effects: Генерирует простые числа
    @raises: None
    @returns: generator — последовательность простых int
    """
    yield 2
    n = 3
    while True:
        is_prime = True
        for d in range(3, int(n**0.5) + 1, 2):
            if n % d == 0:
                is_prime = False
                break
        if is_prime:
            yield n
        n += 2

        
class TestGenerators(unittest.TestCase):
    
    def test_fibo(self):
        #Fibo test
        f = Fibo()
        self.assertEqual(next(f), 0)
        self.assertEqual(next(f), 1)
        self.assertEqual(next(f), 1)
        self.assertEqual(next(f), 2)
    
    def test_integers(self):
        #Integers test
        gen = integers()
        self.assertEqual(next(gen), 0)
        self.assertEqual(next(gen), 1)
        self.assertEqual(next(gen), 2)
    
    def test_primes(self):
        #Primes test
        gen = primes()
        self.assertEqual(next(gen), 2)
        self.assertEqual(next(gen), 3)
        self.assertEqual(next(gen), 5)

if __name__ == '__main__':
    unittest.main(verbosity=2)

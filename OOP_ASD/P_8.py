#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 21:34:15 2026

@author: nadya_urba
"""

from math import gcd as math_gcd
from typing import Dict, Optional


class RatNum:
    '''
    Неизменяемое рациональное число numer/denom в сокращенной форме.
    Representation fields:
    _is_nan: bool - true если NaN
    _numer: int - числитель (если не NaN)
    _denom: int - знаменатель > 0 (если не NaN)
    
    Representation invariant:
    (_is_nan) -> (_numer = 0 ∧ _denom = 1)
    (not _is_nan) -> (_denom > 0 ∧ gcd(|_numer|, _denom) = 1)
    
    Abstraction function:
    если _is_nan: NaN
    иначе: значение _numer/_denom
    '''

    def __init__(self, numer: int = 0, denom: int = 1):
        '''
        @requires: denom != 0 или numer, denom целые
        @modifies: None
        @effects: создает RatNum(numer/denom) в сокращенной форме или NaN
        @throws: None
        @returns: Nan if denom == 0
        '''
        if denom == 0:
            self._is_nan = True
            return
        if denom < 0:
            numer, denom = -numer, -denom
        g = math_gcd(abs(numer), denom)
        self._numer = numer // g
        self._denom = denom // g
        self._is_nan = False


    def is_nan(self):
        '''
        @requires: None
        @modifies: None
        @effects: None
        @throws: None
        @returns: boolean
        '''
        return self._is_nan

    def is_negative(self):
        '''
        @requires: not self.is_nan()
        @modifies: None
        @effects: None
        @throws: None
        @returns: boolean
        '''
        return not self._is_nan and self._numer < 0

    def is_positive(self):
        '''
        @requires: not self.is_nan()
        @modifies: None
        @effects: None
        @throws: None
        @returns: boolean
        '''
        return not self._is_nan and self._numer > 0

    def compare_to(self, other: 'RatNum'):
        '''
        @requires: != Nan
        @modifies: None
        @effects: None
        @throws: None
        @returns: -1 or 0 or 1 - int
        '''
        if self._is_nan or other._is_nan:
            if self._is_nan and other._is_nan:
                return 0
            return 1 if self._is_nan else -1
        left = self._numer * other._denom
        right = other._numer * self._denom
        return -1 if left < right else (1 if left > right else 0)

    def float_value(self):
        '''
        @requires: None
        @modifies: None
        @effects: None
        @throws: None
        @returns: float(self) или NaN
        '''
        return float('nan') if self._is_nan else self._numer / self._denom

    def int_value(self):
        '''
        @requires: None
        @modifies: None
        @effects: None
        @throws: None
        @returns: int or 0 (для NaN)
        '''
        return 0 if self._is_nan else self._numer // self._denom

    def __neg__(self):
        '''
        @requires: None
        @modifies: None
        @effects: None
        @throws: None
        @returns: -self (-NaN = NaN)
        '''
        if self._is_nan:
            return self
        return RatNum(-self._numer, self._denom)

    def __add__(self, other: 'RatNum'):
        '''
        @requires: other != null
        @modifies: None
        @effects: None
        @throws: None
        @returns: self + other (NaN + x = NaN)
        '''
        if self._is_nan or other._is_nan:
            return RatNum(0, 0)
        numer = self._numer * other._denom + other._numer * self._denom
        denom = self._denom * other._denom
        return RatNum(numer, denom)

    def __sub__(self, other: 'RatNum'):
        '''
        @requires: other != null
        @modifies: None
        @effects: None
        @throws: None
        @returns: this - other
        '''
        return self + (-other)

    def __mul__(self, other: 'RatNum'):
        '''
        @requires: other != null
        @modifies: None
        @effects: None
        @throws: None
        @returns: this * other (NaN * x = NaN)
        '''
        if self._is_nan or other._is_nan:
            return RatNum(0, 0)
        return RatNum(self._numer * other._numer, self._denom * other._denom)

    def __truediv__(self, other: 'RatNum'):
        '''
        @requires: other != null
        @modifies: None
        @effects: None
        @throws: None
        @returns: this / other (if other = 0 return NaN)
        '''
        if self._is_nan or other._is_nan or other._numer == 0:
            return RatNum(0, 0)
        return self * RatNum(other._denom, other._numer)

    def gcd(self, other: 'RatNum') -> 'RatNum':
        '''
        @requires: not self.is_nan() and not other.is_nan()
        @modifies: None
        @effects: None
        @throws: None
        @returns: gcd(|this|, |other|) как RatNum
        '''
        if self._is_nan or other._is_nan:
            return RatNum(0, 0)
        return RatNum(math_gcd(abs(self._numer), abs(other._numer)), 1)

    def __str__(self):
        '''
        @requires: None
        @modifies: None
        @effects: None
        @throws: None
        @returns: str ("NaN", "N" или "N/D")
        '''
        if self._is_nan:
            return 'NaN'
        if self._denom == 1:
            return str(self._numer)
        return f'{self._numer}/{self._denom}'

    def __hash__(self):
        '''
        @requires: None
        @modifies: None
        @effects: None
        @throws: None
        @returns: hash(self)
        '''
        if self._is_nan:
            return hash('NaN')
        return hash((self._numer, self._denom))

    def __eq__(self, other):
        '''
        @requires: None
        @modifies: None
        @effects: None
        @throws: None
        @returns: boolean
        '''
        if self._is_nan and isinstance(other, RatNum) and other._is_nan:
            return True
        if self._is_nan or not isinstance(other, RatNum):
            return False
        return self._numer == other._numer and self._denom == other._denom


class RatPoly:
    '''
    Полином с коэффициентами RatNum: a * x**2 + b * x + c.
    Representation fields:
    _coeffs: Dict[int, RatNum] - коэффициенты по степеням
    
    Representation invariant:
    ∀deg∈_coeffs: not coeff[deg].is_nan()
    ∀deg∈_coeffs: coeff[deg] != 0
    если _coeffs пусто: это нулевой полином {} = 0
    
    Abstraction function:
    P(x) = _coeffs[2]*x² + _coeffs[1]*x¹ + _coeffs[0]*x⁰
    '''

    def __init__(self, coeffs: Optional[Dict[int, RatNum]] = None):
        '''
        @requires: coeffs содержит только ненулевые RatNum или null
        @modifies: self
        @effects: создает полином из coeffs, удаляет нули и NaN
        @throws: None
        @returns: self
        '''
        self._coeffs = {}
        if coeffs:
            for deg, coef in coeffs.items():
                if not coef.is_nan():
                    self._coeffs[deg] = coef
        self._normalize()

    def _normalize(self):
        '''Удаление нулевых коэффициентов'''
        to_remove = [deg for deg, coef in list(self._coeffs.items()) 
                     if coef._numer == 0 or coef._denom == 0]
        for deg in to_remove:
            del self._coeffs[deg]
        
    def degree(self):
        '''
        @requires: not self.is_nan()
        @modifies: None
        @effects: None
        @throws: ValueError
        @returns: int - максимальная степень
        '''
        if not self._coeffs:
            return 0
        return max(self._coeffs.keys())

    def get_coeff(self, deg: int):
        '''
        @requires: deg >= 0
        @modifies: None
        @effects: None
        @throws: None
        @returns: self, коэффициент при x^deg
        '''
        return self._coeffs.get(deg, RatNum(0))

    def is_nan(self):
        '''
        @requires: None
        @modifies: None
        @effects: None
        @throws: None
        @returns: boolean, false
        '''
        return False

    def scale_coeff(self, factor: RatNum):
        '''
        @requires: not self.is_nan() and not factor.is_nan()
        @modifies: None
        @effects: None
        @throws: None
        @returns: полином с коэффициентами * factor
        ''' 
        if factor.is_nan():
           return RatPoly({0: RatNum(0, 0)})
        new_coeffs = {deg: coef * factor for deg, coef in self._coeffs.items()}
        return RatPoly(new_coeffs)

    def __neg__(self):
        '''
        @requires: None
        @modifies: None
        @effects: None
        @throws: None
        @returns: -self
        '''
        if self.is_nan():
            return self
        return RatPoly({deg: -coef for deg, coef in self._coeffs.items()})
    
    def __add__(self, other: 'RatPoly'):
        '''
        @requires: other is RatPoly
        @modifies: None
        @effects: None
        @throws: None
        @returns: this + other
        '''
        if self.is_nan() or other.is_nan():
            return RatPoly({0: RatNum(0, 0)})
        coeffs = {**self._coeffs}
        for deg, coef in other._coeffs.items():
            coeffs[deg] = coeffs.get(deg, RatNum(0)) + coef
        return RatPoly(coeffs)

    def __sub__(self, other: 'RatPoly'):
        '''
        @requires: other is RatPoly
        @modifies: None
        @effects: None
        @throws: None
        @returns: this - other
        '''
        return self + (-other)

    def __mul__(self, other: 'RatPoly'):
        '''
        @requires: other is RatPoly
        @modifies: None
        @effects: None
        @throws: None
        @returns: this * other
        '''
        if self.is_nan() or other.is_nan():
            return RatPoly({0: RatNum(0, 0)})
        coeffs = {}
        for d1, c1 in self._coeffs.items():
            for d2, c2 in other._coeffs.items():
                deg = d1 + d2
                coeffs[deg] = coeffs.get(deg, RatNum(0)) + c1 * c2
        return RatPoly(coeffs)

    def __truediv__(self, other: 'RatPoly'):
        '''
        @requires: other is RatPoly
        @modifies: None
        @effects: None
        @throws: ValueError
        @returns: частное от деления
        '''
        raise ValueError("Деление полиномов не реализовано")


    def eval(self, x: RatNum):
        '''
        @requires: not self.is_nan()
        @modifies: None
        @effects: None
        @throws: None
        @returns: P(x)
        '''
        result = RatNum(0)
        px = RatNum(1)
        max_deg = 0
        if self._coeffs:
            max_deg = max(self._coeffs.keys())
        for deg in range(max_deg + 1):
            result = result + self.get_coeff(deg) * px
            px = px * x
        return result

    def differentiate(self):
        '''
        @requires: None
        @modifies: None
        @effects: None
        @throws: None
        @returns: P'(x)
        '''
        if self.is_nan() or self.degree() == 0:
            return RatPoly()
        coeffs = {}
        for deg, coef in self._coeffs.items():
            if deg > 0:
                coeffs[deg - 1] = coef * RatNum(deg)
        return RatPoly(coeffs)
    

    def anti_differentiate(self):
        '''
        @requires: None
        @modifies: None
        @effects: None
        @throws: None
        @returns: первообразная
        '''
        coeffs = {}
        for deg, coef in self._coeffs.items():
            new_deg = deg + 1
            new_coef = coef / RatNum(new_deg)
            coeffs[new_deg] = new_coef
        return RatPoly(coeffs)

    def integrate(self, a: RatNum, b: RatNum) -> RatNum:
        '''
        @requires: not self.is_nan()
        @modifies: None
        @effects: None
        @throws: None
        @returns: интеграл от a до b
        '''
        anti = self.anti_differentiate()
        return anti.eval(b) - anti.eval(a)

    def value_of(self, x: RatNum) -> RatNum:
        '''
        @requires: None
        @modifies: None
        @effects: None
        @throws: None
        @returns: P(x)
        '''
        return self.eval(x)

    def __str__(self):
        if not self._coeffs:
            return '0'
        
        terms = []
        for deg in sorted(self._coeffs.keys(), reverse=True):
            coef = self._coeffs[deg]
            coef_str = str(coef)
            
            if deg == 0:
                terms.append(coef_str)
            elif deg == 1:
                if coef_str == '1':
                    terms.append('x')
                elif coef_str == '-1':
                    terms.append('-x')
                else:
                    terms.append(coef_str + 'x')
            else:
                terms.append(coef_str + f'x^{deg}')
        
        result = '+'.join(terms).replace('+-', '-')
        return result if result != '0/1' else '0'
    
    def __hash__(self):
        '''
        @requires: None
        @modifies: None
        @effects: None
        @throws: None
        @returns: hash(self)
        '''
        return hash(frozenset(self._coeffs.items()))

    def __eq__(self, other):
        '''
        @requires: None
        @modifies: None
        @effects: None
        @throws: None
        @returns: boolean
        '''
        if not isinstance(other, RatPoly):
            return False
        if self.is_nan() != other.is_nan():
            return False
        return self._coeffs == other._coeffs
    
# Модульные тесты

print("TESTING RATNUM")

# Test 1: Creation
expected = "2/3"
actual = str(RatNum(12, 18))
if expected != actual:
    print("Test 1 FAILED: expected 2/3")
else:
    print("Test 1 PASSED")

# Test 2: NaN detection
expected = True
actual = RatNum(0, 0).is_nan()
if expected != actual:
    print("Test 2 FAILED: 0/0 should be NaN")
else:
    print("Test 2 PASSED")

# Test 3: is_negative()
expected = True
actual = RatNum(-1, 2).is_negative()
if expected != actual:
    print("Test 3 FAILED: -1/2 should be negative")
else:
    print("Test 3 PASSED")

# Test 4: is_positive()
expected = True
actual = RatNum(1, 2).is_positive()
if expected != actual:
    print("Test 4 FAILED: 1/2 should be positive")
else:
    print("Test 4 PASSED")

# Test 5: compare_to()
expected = 1
actual = RatNum(1, 2).compare_to(RatNum(1, 3))
if expected != actual:
    print("Test 5 FAILED: 1/2 > 1/3 should return 1")
else:
    print("Test 5 PASSED")

# Test 6: float_value()
expected = 0.5
actual = RatNum(1, 2).float_value()
if expected != actual:
    print("Test 6 FAILED: float_value(1/2) should be 0.5")
else:
    print("Test 6 PASSED")

# Test 7: int_value()
expected = 0
actual = RatNum(1, 2).int_value()
if expected != actual:
    print("Test 7 FAILED: int_value(1/2) should be 0")
else:
    print("Test 7 PASSED")

# Test 8: __neg__()
expected = "-1/2"
actual = str(-RatNum(1, 2))
if expected != actual:
    print("Test 8 FAILED: -1/2 unary minus")
else:
    print("Test 8 PASSED")

# Test 9: __add__()
expected = "5/6"
actual = str(RatNum(1, 2) + RatNum(1, 3))
if expected != actual:
    print("Test 9 FAILED: 1/2 + 1/3 = 5/6")
else:
    print("Test 9 PASSED")

# Test 10: __sub__()
expected = "1/6"
actual = str(RatNum(1, 2) - RatNum(1, 3))
if expected != actual:
    print("Test 10 FAILED: 1/2 - 1/3 = 1/6")
else:
    print("Test 10 PASSED")

# Test 11: __mul__()
expected = "1/6"
actual = str(RatNum(1, 2) * RatNum(1, 3))
if expected != actual:
    print("Test 11 FAILED: 1/2 * 1/3 = 1/6")
else:
    print("Test 11 PASSED")

# Test 12: __truediv__()
expected = "3/2"
actual = str(RatNum(1, 2) / RatNum(1, 3))
if expected != actual:
    print("Test 12 FAILED: 1/2 / 1/3 = 3/2")
else:
    print("Test 12 PASSED")

# Test 13: gcd()
expected = "6"
actual = str(RatNum(12).gcd(RatNum(18)))
if expected != actual:
    print("Test 13 FAILED: gcd(12,18) = 6")
else:
    print("Test 13 PASSED")

# Test 14: __str__()
expected = "NaN"
actual = str(RatNum(0, 0))
if expected != actual:
    print("Test 14 FAILED: NaN string representation")
else:
    print("Test 14 PASSED")

# Test 15: __eq__()
r1 = RatNum(1, 2)
r2 = RatNum(2, 4)
expected = True
actual = (r1 == r2)
if expected != actual:
    print("Test 15 FAILED: 1/2 == 2/4")
else:
    print("Test 15 PASSED")

print("\nTESTING RATPOLY")

# Test 16: Polynomial creation
expected = "x+1"
actual = str(RatPoly({1: RatNum(1), 0: RatNum(1)}))
if expected != actual:
    print("Test 16 FAILED: x+1 representation")
else:
    print("Test 16 PASSED")

# Test 17: degree()
expected = 1
actual = RatPoly({1: RatNum(1), 0: RatNum(1)}).degree()
if expected != actual:
    print("Test 17 FAILED: degree of x+1 should be 1")
else:
    print("Test 17 PASSED")

# Test 18: get_coeff()
expected = RatNum(1)
actual = RatPoly({1: RatNum(1)}).get_coeff(1)
if expected != actual:
    print("Test 18 FAILED: coefficient of x")
else:
    print("Test 18 PASSED")
'''
# Test 19: is_nan()
expected = True
actual = RatPoly({0: RatNum(0, 0)}).is_nan()
if expected != actual:
    print("Test 19 FAILED: NaN polynomial")
else:
    print("Test 19 PASSED")
'''
# Test 20: scale_coeff()
expected = "2x+2"
actual = str(RatPoly({1: RatNum(1), 0: RatNum(1)}).scale_coeff(RatNum(2)))
if expected != actual:
    print("Test 20 FAILED: scale coefficients by 2")
else:
    print("Test 20 PASSED")

# Test 21: __add__()
expected = "2x+2"
actual = str(RatPoly({1: RatNum(1), 0: RatNum(1)}) + RatPoly({1: RatNum(1), 0: RatNum(1)}))
if expected != actual:
    print("Test 21 FAILED: polynomial addition")
else:
    print("Test 21 PASSED")

# Test 22: __mul__()
expected = "1x^2+2x+1"
actual = str(RatPoly({1: RatNum(1), 0: RatNum(1)}) * RatPoly({1: RatNum(1), 0: RatNum(1)}))
if expected != actual:
    print("Test 22 FAILED: polynomial multiplication")
else:
    print("Test 22 PASSED")

# Test 23: eval()
expected = "3"
actual = str(RatPoly({1: RatNum(1), 0: RatNum(1)}).eval(RatNum(2)))
if expected != actual:
    print("Test 23 FAILED: eval(x+1, x=2)")
else:
    print("Test 23 PASSED")

# Test 24: differentiate()
expected = "2x+2"
actual = str(RatPoly({2: RatNum(1), 1: RatNum(2), 0: RatNum(3)}).differentiate())
if expected != actual:
    print("Test 24 FAILED: derivative")
else:
    print("Test 24 PASSED")

# Test 25: anti_differentiate()
expected = "1/3x^3+1x^2+3x"
actual = str(RatPoly({2: RatNum(1), 1: RatNum(2), 0: RatNum(3)}).anti_differentiate())
if expected != actual:
    print("Test 25 FAILED: antiderivative")
else:
    print("Test 25 PASSED")

# Test 26: integrate()
expected = "2"
actual = str(RatPoly({1: RatNum(2), 0: RatNum(1)}).integrate(RatNum(0), RatNum(1)))
if expected != actual:
    print("Test 26 FAILED: definite integral")
else:
    print("Test 26 PASSED")

print("\nALL TESTS COMPLETED")


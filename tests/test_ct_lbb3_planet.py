'''test_planet.py'''

import unittest
import sys
import os
from ehex import ehex
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
from traveller_api.ct.lbb3.worldgen.planet import System


class TestCreate(unittest.TestCase):
    '''Test create planet object'''

    def test_bare_create(self):
        '''Test basic create'''
        system = System()
        self.assertTrue(isinstance(system, System))

    def test_name_create(self):
        '''Test create with name'''
        system = System(name='Chulak')
        self.assertEqual(system.name, 'Chulak')

    def test_uwp_create(self):
        '''Test create with UWP'''
        system = System(name='Chulak', uwp='D758565-3')
        self.assertEqual(system.starport, 'D')
        self.assertEqual(int(system.size), 7)
        self.assertEqual(int(system.atmosphere), 5)
        self.assertEqual(int(system.hydrographics), 8)
        self.assertEqual(int(system.population), 5)
        self.assertEqual(int(system.government), 6)
        self.assertEqual(int(system.lawlevel), 5)
        self.assertEqual(int(system.techlevel), 3)

    def test_str(self):
        '''Test str() representation'''
        uwp = 'D758565-3'
        system = System(uwp=uwp)
        self.assertEqual(str(system), uwp)

    def test_bogus_uwp_create(self):
        '''Test create with bogus UWP'''
        uwp = 'P999'
        with self.assertRaises(TypeError):
            system = System(uwp=uwp)
            del system

    def test_characteristics(self):
        '''Test characteristics types'''
        system = System(uwp='D77A77A-A')
        self.assertTrue(isinstance(system.starport, str))
        self.assertTrue(isinstance(system.size, ehex))
        self.assertTrue(isinstance(system.atmosphere, ehex))
        self.assertTrue(isinstance(system.hydrographics, ehex))
        self.assertTrue(isinstance(system.population, ehex))
        self.assertTrue(isinstance(system.government, ehex))
        self.assertTrue(isinstance(system.lawlevel, ehex))
        self.assertTrue(isinstance(system.techlevel, ehex))


class TestTradeClassifications(unittest.TestCase):
    '''Test trade classiications'''

    def test_Ag(self):
        '''Test Ag code'''
        system = System(uwp='D600066-6')
        for atm in '456789':
            for hyd in '45678':
                for pop in '567':
                    system.atmosphere = ehex(atm)
                    system.hydrographics = ehex(hyd)
                    system.population = ehex(pop)
                    system._determine_trade_codes()
                    self.assertTrue('Ag' in system.trade_codes)

    def test_not_Ag(self):
        '''Test !Ag code'''
        system = System(uwp='D600066-6')
        for atm in '0123ABC':
            for hyd in '01239A':
                for pop in '0123489A':
                    system.atmosphere = ehex(atm)
                    system.hydrographics = ehex(hyd)
                    system.population = ehex(pop)
                    system._determine_trade_codes()
                    self.assertFalse('Ag' in system.trade_codes)

    def test_Na(self):
        '''Test Na'''
        system = System(uwp='D600066-6')
        for atm in '012':
            for hyd in '0123':
                for pop in '6789A':
                    system.atmosphere = ehex(atm)
                    system.hydrographics = ehex(hyd)
                    system.population = ehex(pop)
                    system._determine_trade_codes()
                    self.assertTrue('Na' in system.trade_codes)

    def test_not_Na(self):
        '''Test !Na'''
        system = System(uwp='D600066-6')
        for atm in '3456789ABC':
            for hyd in '456789A':
                for pop in '012345':
                    system.atmosphere = ehex(atm)
                    system.hydrographics = ehex(hyd)
                    system.population = ehex(pop)
                    system._determine_trade_codes()
                    self.assertFalse('Na' in system.trade_codes)

    def test_In(self):
        '''Test In code'''
        system = System(uwp='D606066-6')
        for atm in '012479':
            for pop in '9A':
                    system.atmosphere = ehex(atm)
                    system.population = ehex(pop)
                    system._determine_trade_codes()
                    self.assertTrue('In' in system.trade_codes)

    def test_not_In(self):
        '''Test !In code'''
        system = System(uwp='D606066-6')
        for atm in '3568ABC':
            for pop in '012345678':
                    system.atmosphere = ehex(atm)
                    system.population = ehex(pop)
                    system._determine_trade_codes()
                    self.assertFalse('In' in system.trade_codes)

    def test_Ni(self):
        '''Test Ni code'''
        system = System(uwp='D666066-6')
        for pop in '0123456':
            system.population = ehex(pop)
            self.assertTrue('Ni' in system.trade_codes)

    def test_not_Ni(self):
        '''Test !Ni code'''
        system = System(uwp='D666066-6')
        for pop in '789A':
            system.population = ehex(pop)
            system._determine_trade_codes()
            self.assertFalse('Ni' in system.trade_codes)

    def test_Ri(self):
        '''Test Ri'''
        system = System(uwp='D707007-7')
        for gov in '456789':
            for atm in '68':
                for pop in '678':
                    system.government = ehex(gov)
                    system.atmosphere = ehex(atm)
                    system.population = ehex(pop)
                    system._determine_trade_codes()
                    self.assertTrue('Ri' in system.trade_codes)

    def test_not_Ri(self):
        '''Test "Ri'''
        system = System(uwp='D707007-7')
        for gov in '0123ABCDE':
            for atm in '01234579ABC':
                for pop in '0123459A':
                    system.government = ehex(gov)
                    system.atmosphere = ehex(atm)
                    system.population = ehex(pop)
                    system._determine_trade_codes()
                    self.assertFalse('Ri' in system.trade_codes)

    def test_Po(self):
        '''Test Po'''
        system = System(uwp='D700777-7')
        for atm in '2345':
            for hyd in '0123':
                system.atmosphere = ehex(atm)
                system.hydrographics = ehex(hyd)
                system._determine_trade_codes()
                self.assertTrue('Po' in system.trade_codes)

    def test_not_Po(self):
        '''Test !Po'''
        system = System(uwp='D700777-7')
        for atm in '016789ABC':
            for hyd in '456789A':
                system.atmosphere = ehex(atm)
                system.hydrographics = ehex(hyd)
                system._determine_trade_codes()
                self.assertFalse('Po' in system.trade_codes)

    def test_Wa(self):
        '''Test Wa'''
        system = System(uwp='D77A777-7')
        self.assertTrue('Wa' in system.trade_codes)

    def test_not_Wa(self):
        '''Test !Wa'''
        system = System(uwp='D770777-7')
        for hyd in '0123456789':
            system.hydrographics = ehex(hyd)
            system._determine_trade_codes()
            self.assertFalse('Wa' in system.trade_codes)

    def test_De(self):
        '''Test De'''
        system = System(uwp='D770777-7')
        self.assertTrue('De' in system.trade_codes)

    def test_not_De(self):
        '''Test !De'''
        system = System(uwp='D770777-7')
        for hyd in '123456789':
            system.hydrographics = ehex(hyd)
            system._determine_trade_codes()
            self.assertFalse('De' in system.trade_codes)

    def test_Va(self):
        '''Test Va'''
        system = System(uwp='D700777-7')
        self.assertTrue('Va' in system.trade_codes)

    def test_not_Va(self):
        '''Test !Va'''
        system = System(uwp='D707777-7')
        for atm in '123456789ABC':
            system.atmosphere = ehex(atm)
            system._determine_trade_codes()
            self.assertFalse('Va' in system.trade_codes)

    def test_As(self):
        '''Test As'''
        system = System(uwp='D000777-7')
        self.assertTrue('As' in system.trade_codes)

    def test_not_As(self):
        '''Test !As'''
        system = System(uwp='D077777-7')
        for siz in '123456789A':
            system.size = ehex(siz)
            system._determine_trade_codes()
            self.assertFalse('As' in system.trade_codes)

    def test_Ic(self):
        '''Test Ic'''
        system = System(uwp='D700777-7')
        for atm in '01':
            for hyd in '123456789A':
                system.atmosphere = ehex(atm)
                system.hydrographics = ehex(hyd)
                system._determine_trade_codes()
                self.assertTrue('Ic' in system.trade_codes)

    def test_not_Ic(self):
        '''Test !Ic'''
        system = System(uwp='D700777-7')
        for atm in '23456789ABC':
            system.atmosphere = ehex(atm)
            system._determine_trade_codes()
            self.assertFalse('Ic' in system.trade_codes)

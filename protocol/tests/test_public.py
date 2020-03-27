#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2020/3/26 15:27
# @Author  : Lancer

import unittest
import logging
import  sys
sys.path.append("..")
from parserprotocol.public  import  *

class test_public(unittest.TestCase):
    def  test_strtolist(self):
        self.assertEqual([0x88,0x55,0xaa],  strtolist("8855aa"))
        self.assertEqual([0x88, 0x55, 0xaa], strtolist("  885 5aa  "))
        self.assertEqual( None, strtolist("8855aa 7"))

    def  test_toStr(self):
        self.assertEqual( "10", toStr(16,16))
        self.assertEqual("A", toStr(10, 16))

    def test_bytes_steam_to_value(self):
        desc_table = [
            ["类型",2 ],
            ["长度",2 ]
        ]
        ret =  bytes_steam_to_value([0x31,0x04,0x55,0],0, desc_table)
        print("0x%x"%ret["类型"])
        print("0x%x" %ret["长度"])
        pass

    def  test_get_bytes(self):
        self.assertEqual(0x55 ,get_bytes([0x55,0xaa,0x00,0x05], 1))
        self.assertEqual(0x55aa, get_bytes([0x55, 0xaa, 0x00, 0x05], 2))
        self.assertEqual(0xaa, get_bytes([0x55, 0xaa, 0x00, 0x05], 1,roffset=1))

    def   test_get_bit(self):
        self.assertEqual(0x0F, get_bit([0xF0,0xaa,0x55], 4,0 ))
        self.assertEqual(0x02, get_bit([0xF0, 0xaa, 0x55], 2, 8))


    def   test_bit_steam_to_value(self):
        desc_table = [
            ["类型",2 ],
            ["长度",2 ]
        ]
        ret = bit_steam_to_value([0xC0,0xA5], 0, desc_table) # 11 00
        self.assertEqual(0x03, ret["类型"])
        self.assertEqual(0x00, ret["长度"])






if __name__ == "__main__":
    unittest.main()
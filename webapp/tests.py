from django.test import TestCase

# Create your tests here.
import logging

import os


a=("id","kw")

def find_element(*loc):
    aaa = loc
    print aaa


find_element('id','kw')
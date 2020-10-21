import os
import sys
import argparse
import constants
import random


class Cell(object):

    def __init__(self, col, row):
        """
            Args:
               has_honey - boolean, indicates presence of honey
               has_bear - boolean, indicates presence of bear
        """
        self.has_honey = False
        self.bear = None
        self.col = col
        self.row = row

    def set_bear(self, bear):
        self.bear = bear

    def remove_bear(self):
        self.bear = None

    def is_empty(self):
        res = (not self.has_honey) and (self.bear is None)
        return res

    def has_honey(self):
        return self.has_honey

    def has_bear(self):
        return self.bear

    def set_honey(self):
        self.has_honey = True

    def remove_honey(self):
        self.has_honey = False

    def get_bear(self):
        return self.bear


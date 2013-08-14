#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe

setup(windows = ['D:\Learning_Library\Python\WirelessShow\WirelessShow.py'],
		data_files = [('image',['D:\Learning_Library\Python\WirelessShow\splash.jpg'])])
'''
Created on 2021-04-11 21:37:48
Last modified on 2021-04-24 20:32:03

@author: L. F. Pereira (luisfgpereira95@gmail.com)
'''

# imports

# standard library
import setuptools


NAME = 'pyutils'
VERSION = '0.0.1'
AUTHOR = 'L. F. Pereira'
AUTHOR_EMAIL = 'luisfgpereira95@gmail.com'

# setup

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},

)

# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '1.5'

setup(name='upc.genweb.soa',
      version=version,
      description="",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='UPCnet Plone Team',
      author_email='plone.team@upcnet.es',
      url='https://github.com/upcnet/upcnet.genweb.soa',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['upc', 'upc.genweb'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'suds',
          'z3c.suds'
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

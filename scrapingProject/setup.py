# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name         = 'project',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = scrapingProject.settings']},
      #package_dir = {'JSscripts': 'scrapingProject/JSscripts'},
    package_data = {'scrapingProject': ['JSscripts/*.js']},
)

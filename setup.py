import sys
from setuptools import setup

if sys.version_info < (3, 6):
    sys.exit('Sorry, tin-score-calculation requires Python >= 3.6')

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='tin-score-calculation',
    version='0.5',
    description="",
    url='',
    include_package_data=True,
    scripts=['scripts/calculate-tin.py', 'scripts/merge-tin.py', 'scripts/plot-tin.py'],
    install_requires=required,
    keywords='tin-score-calculation',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ]
)

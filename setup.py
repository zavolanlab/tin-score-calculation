import sys
from setuptools import setup

if sys.version_info < (3, 6):
    sys.exit('Sorry, tin-score-calculation requires Python >= 3.6')

requirements = [
    "bx-python>=0.8.10",
    "guppy3>=3.1.0",
    "matplotlib>=3.3.4",
    "pandas>=1.2.3",
    "psutil>=5.8.0",
    "pysam>=0.16.0.1",
    "RSeQC>=3.0.1",
]

setup(
    name='tin-score-calculation',
    version='0.4',
    description="",
    url='',
    include_package_data=True,
    scripts=['scripts/calculate-tin.py', 'scripts/merge-tin.py', 'scripts/plot-tin.py'],
    install_requires=requirements,
    keywords='tin-score-calculation',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ]
)

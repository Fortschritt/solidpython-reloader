from setuptools import setup

setup(
    scripts=['bin/sp-reloader',],
    entry_points = {
        'console_scripts': ['sp-reloader=spreloader.command_line:main'],
    },
    install_requires=[
   'Django>=2.2,<2.3',
   'solidpython'
    ],
)

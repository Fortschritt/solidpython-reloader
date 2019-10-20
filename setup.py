from setuptools import setup, find_packages

setup(
    scripts=['bin/sp-reloader',],
    entry_points = {
        'console_scripts': ['sp-reloader=spreloader.command_line:main'],
    },
    install_requires=[
   'Django>=2.2,<2.3',
   'solidpython'
    ],
    include_package_data=True,
    packages=find_packages(include=['spreloader',]),
)

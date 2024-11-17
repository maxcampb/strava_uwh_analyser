import setuptools
from setuptools import find_packages

with open("./requirements/requirements.in", "r") as req_file:
    REQUIREMENTS = req_file.read().splitlines()

setuptools.setup(
    name="strava_uwh_analyser",
    version='0.0.1',
    description='This is a package to analyse training and build reports for underwater hockey players using strava data',
    url='https://github.com/maxcampb/strava_uwh_analyser',
    author='Max Campbell',
    author_email='maxcampbe@gmail.com',
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    python_requires='>=3.10',
    classifiers=[
        "Development Status :: 2 Pre-Alpha",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=REQUIREMENTS,
    package_data={
        "": ["*"],
    },
    entry_points={
        # Add your report here
        'console_scripts': [
            'run_gb_uwh_report = strava_uwh_analyser.main:run_gb_uwh_report'
        ]
    }
)

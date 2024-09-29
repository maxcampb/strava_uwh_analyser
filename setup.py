import setuptools
from setuptools import find_packages

with open("./requirements/requirements.in", "r") as req_file:
    REQUIREMENTS = req_file.read().splitlines()

REQUIREMENTS.append("helper_max")

setuptools.setup(
    name="{strava_uwh_analyser}",
    version='0.0.1',
    description='your description HERE',
    url='https://github.com/{USER}/{strava_uwh_analyser}',
    author='Max Campbell',
    author_email='maxcampbe@gmail.com',
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    python_requires='>=3.9',
    classifiers=[
        "Development Status :: 2 Pre-Alpha",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=REQUIREMENTS,
    package_data={"": ["*"]},
    entry_points={
        'console_scrips': [
            'name_of_task = {strava_uwh_analyser}.main:main'
        ]
    }
)

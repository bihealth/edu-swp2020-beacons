# CUBI Education: SWP Bioinformatik Beacons
The SWP Beacon Project is a Software which allows users to ask for the existence of given variants thereby it uses the Beacon protocol.

## Getting Started for v.2.0.0

These instructions will get you a copy of the project  and how to get the system running on your local machine for testing purposes. 

### Prerequisites and Installing

Please clone the repository edu-swp2020-beacon on git and navigate to the edu-swp2020-beacon file:

```
$ git clone git@github.com:bihealth/edu-swp2020-beacons.git
$ cd edu-swp2020-beacons
```
The application is running with Python, so a version of installed Python >= 3.6.0 is required. Use pipenv for installing the required packages in the Pipfile:

```
$ pipenv --python python3
$ pipenv shell 
$ pipenv install
```


### Running the tests

If you like to see if your installation was successfully, run the tests: 

```
$ pytest .
```

## Usage

### Web interface


start web_ui.py

```
$ python -m beacon.web_ui
```
start “rest_api.py” in another terminal

```
$ python -m beacon.rest_api
```

fill in variant into the fields of the web interface

click submit to see the results of the search

to repeat, click “go Home” button 

### Command line interface

start “rest_api.py” 

```
$ python -m beacon.rest_api
```

start “user_cli.py” in another terminal

```
$ python -m beacon.user_cli
```

follow instructions on the command line

### Maintaining database

To see which flag you can use, call:

```
$ python3 -m beacon.admin_cli -h 
DB Path:*give "data.db" for maintaining the variant database*
or
DB Path:*give "login.db" for maintaining the user database*
```
If you want to use a new database or a different one, go to settings.py and change manually the variants PATH_DATABASE and PATH_LOGIN accordingly. 

## Authors

* **Namuun**
* **Leylanur**
* **Julia**  
* **Leonardo**
* **Jin Soo**  

Contributor who participated in this project Holtgrewe, Manuel.

## Acknowledgments

* We are thankful for the inspiration and continuous help of our supervisor Manuel
* If you have any concerns or you need help with the software contact him
* Thank you for using our software :))))


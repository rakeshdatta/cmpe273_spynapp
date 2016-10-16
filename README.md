# cmpe273_spynapp

  Python Application is Spyne Toolkit (http://spyne.io/).
  Input message type is  HTTPRPC  and output message type is JSON
  
Installation
============
  Clone repository, create virtualenv and install requirements:
  pip install -r requirements.txt

Usage
=====
  Run the wsgi server along with the app using './app.py'.
  curl 'http://127.0.0.1:8000/checkcrime?lat=<latitude value>lon=<longitude value>&radius=<radius value>

  Here is a Spyne call example
  curl 'http://127.0.0.1:8000/checkcrime?lat=37.334164&lon=-121.884301&radius=0.02'

 
  OUTPUT:
  {
	"event_time_count": {
		"3:01pm-6pm": 2,
		"6:01am-9am": 0,
		"3:01am-6am": 0,
		"12:01pm-3pm": 2,
		"6:01pm-9pm": 1,
		"9:01am-12noon": 3,
		"9:01pm-12midnight": 42,
		"12:01am-3am": 0
	},
	"crime_type_count": {
		"Theft": 5,
		"Arrest": 2,
		"Assault": 6,
		"Other": 35,
		"Robbery": 1,
		"Burglary": 1
	},
	"total_crime": 50,
	"the_most_dangerous_streets": ["N 1ST ST", "E SANTA CLARA ST", "S 1ST ST"]
  }

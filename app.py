#!/usr/bin/env python

import requests
import pprint
import json
import re
from operator import itemgetter
from collections import OrderedDict
from datetime import datetime
from spyne import Application, srpc, ServiceBase, Iterable, UnsignedInteger, \
    String

from spyne.protocol.json import JsonDocument
from spyne.protocol.http import HttpRpc
from spyne.server.wsgi import WsgiApplication


class crimeDataService(ServiceBase):
    @srpc(String, String, String, _returns=String)
    def checkcrime(lat, lon, radius):

            ################# Construct the API url  ######################
            mainurl = "https://api.spotcrime.com/crimes.json?"
            laturl  = "lat=%s&" % lat
            lonurl  = "lon=%s&" % lon
            radurl  = "radius=%s" % radius
	    key     = "&key=."
            url     =  mainurl + laturl + lonurl + radurl + key

            ################ Send the GET request to the crime server #####
            data = requests.get(url)

            ################ Parse the response ###########################
            datajson = json.loads(data.text)
          
            finaljson = {}
            ######## 1. Find total number of crimes ######### 
            finaljson['total_crime'] = len(datajson['crimes'])



            ######## 2. Find the most dangerous streets #####
	    addrjson = {}
	    for indvCrime in datajson['crimes']:
		addr = indvCrime['address']
	    	start = 0
		if re.search("BLOCK OF" , addr):
			start = addr.find('BLOCK OF') + 9
		elif re.search("BLOCK" , addr):
			start = addr.find('BLOCK') + 6

		end	 = len(addr)
		result 	 = addr[start:end]
		finalres = result.replace("BLOCK","")
		addrjson[finalres] = addrjson.get(finalres, 0) + 1

	    sortedaddr = OrderedDict(sorted(addrjson.items(), key=itemgetter(1), reverse=True))
            #print sortedaddr 

            i = len(sortedaddr)
	    if i == 1:
               finaljson['the_most_dangerous_streets'] = sortedaddr.keys()[0] 
            elif i == 2:
               finaljson['the_most_dangerous_streets'] = sortedaddr.keys()[0], \
							 sortedaddr.keys()[1]
            elif i >= 3:
               finaljson['the_most_dangerous_streets'] = sortedaddr.keys()[0], \
							 sortedaddr.keys()[1], \
							 sortedaddr.keys()[2]



            ######## 3. Find crime type count  ##############
	    finaljson['crime_type_count'] = {}
            for indvCrime in datajson['crimes']:
                crime_type = indvCrime['type']
	        finaljson['crime_type_count'][crime_type] = finaljson['crime_type_count'].get(crime_type,0) + 1



            ######## 4. Find event time count  ##############
	    finaljson['event_time_count'] = {}
	    finaljson['event_time_count']['12:01am-3am']       = 0	
	    finaljson['event_time_count']['3:01am-6am']        = 0	
	    finaljson['event_time_count']['6:01am-9am']        = 0	
	    finaljson['event_time_count']['9:01am-12noon']     = 0	
	    finaljson['event_time_count']['12:01pm-3pm']       = 0	
	    finaljson['event_time_count']['3:01pm-6pm']        = 0	
	    finaljson['event_time_count']['6:01pm-9pm']        = 0	
	    finaljson['event_time_count']['9:01pm-12midnight'] = 0	

            t1  = datetime.strptime("12:01 AM", "%I:%M %p").time()
            t2  = datetime.strptime("03:00 AM", "%I:%M %p").time()
            t3  = datetime.strptime("03:01 AM", "%I:%M %p").time()
            t4  = datetime.strptime("06:00 AM", "%I:%M %p").time()
            t5  = datetime.strptime("06:01 AM", "%I:%M %p").time()
            t6  = datetime.strptime("09:00 AM", "%I:%M %p").time()
            t7  = datetime.strptime("09:01 AM", "%I:%M %p").time()
            t8  = datetime.strptime("12:00 PM", "%I:%M %p").time()
            t9  = datetime.strptime("12:01 PM", "%I:%M %p").time()
            t10 = datetime.strptime("03:00 PM", "%I:%M %p").time()
            t11 = datetime.strptime("03:01 PM", "%I:%M %p").time()
            t12 = datetime.strptime("06:00 PM", "%I:%M %p").time()
            t13 = datetime.strptime("06:01 PM", "%I:%M %p").time()
            t14 = datetime.strptime("09:00 PM", "%I:%M %p").time()
            t15 = datetime.strptime("09:01 PM", "%I:%M %p").time()
            t16 = datetime.strptime("11:59 PM", "%I:%M %p").time()
            t17 = datetime.strptime("12:00 AM", "%I:%M %p").time()

            range1 = '12:01am-3am'
            for indvCrime in datajson['crimes']:
                crimeDatetime = indvCrime['date']
                crimeTime = datetime.strptime(crimeDatetime, "%m/%d/%y %I:%M %p").time()

                if t1 <= crimeTime <= t2:
			finaljson['event_time_count']['12:01am-3am'] =  \
				int(finaljson['event_time_count']['12:01am-3am']) + int(1)
			continue
                if t3 <= crimeTime <= t4:
			finaljson['event_time_count']['3:01am-6am'] =  \
				int(finaljson['event_time_count']['3:01am-6am']) + int(1)
			continue
                if t5 <= crimeTime <= t6:
			finaljson['event_time_count']['6:01am-9am'] =  \
				int(finaljson['event_time_count']['6:01am-9am']) + int(1)
			continue
                if t7 <= crimeTime <= t8:
			finaljson['event_time_count']['9:01am-12noon'] =  \
				int(finaljson['event_time_count']['9:01am-12noon']) + int(1)
			continue
                if t9 <= crimeTime <= t10:
			finaljson['event_time_count']['12:01pm-3pm'] =  \
				int(finaljson['event_time_count']['12:01pm-3pm']) + int(1)
			continue
                if t11 <= crimeTime <= t12:
			finaljson['event_time_count']['3:01pm-6pm'] =  \
				int(finaljson['event_time_count']['3:01pm-6pm']) + int(1)
			continue
                if t13 <= crimeTime <= t14:
			finaljson['event_time_count']['6:01pm-9pm'] =  \
				int(finaljson['event_time_count']['6:01pm-9pm']) + int(1)
			continue
                if t15 <= crimeTime <= t16:
			finaljson['event_time_count']['9:01pm-12midnight'] =  \
				int(finaljson['event_time_count']['9:01pm-12midnight']) + int(1)
			continue
                if crimeTime == t17:
			finaljson['event_time_count']['9:01pm-12midnight'] =  \
				int(finaljson['event_time_count']['9:01pm-12midnight']) + int(1)
			continue


            ################################################################
            return finaljson

            ######################## END OF checkcrime() ########################################



if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    app = Application([crimeDataService], 
		      'spyne.examples.hello.http',
          	       in_protocol=HttpRpc(validator='soft'),
        	       out_protocol=JsonDocument(ignore_wrappers=True),
    		     )

    wsgi_application = WsgiApplication(app)

    server = make_server('127.0.0.1', 8000, wsgi_application)

    print "server started on http://127.0.0.1:8000"

    server.serve_forever()

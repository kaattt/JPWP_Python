#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient
from sgmllib import SGMLParser
#import sgmllib

import tornado.httpserver
import tornado.ioloop
import tornado.web

from pprint import pprint
import json
import traceback
# 

# klasa-widok
class MainHandler(tornado.web.RequestHandler):
	def post(self):
		# dodałem obsługę błędów parsowania JSON....
		try:
			data_json = tornado.escape.json_decode(self.request.body)
			content = data_json['content']
			countryFound = re.search("country\((.+?)\)", content)
			tagFound = re.search("tag\((.+?)\)", content)
			
			if countryFound:
				country = countryFound.group(1)
			print 'Country: ' + country 
			
			if tagFound:
				tag = tagFound.group(1)
			print 'TAG: ' + tag 
			
			self.write(data_json)
			#pprint (data_json)
		except Exception, e:
			self.write(json.dumps({'status': 'fail', 'error': "Error occured:\n%s" % traceback.format_exc()}))
# mapowanie URLi
application = tornado.web.Application([
    (r"/", MainHandler),])

if __name__ == "__main__":
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	tornado.ioloop.IOLoop.instance().start()


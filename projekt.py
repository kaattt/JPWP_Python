#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient
from sgmllib import SGMLParser
import requests


import tornado.httpserver
import tornado.ioloop
import tornado.web

import json
import traceback


client = MongoClient()

def getCountryInfo(country):
	page = urllib2.urlopen("http://en.wikipedia.org/wiki/" +country)
	htmlSource = page.read()
	page.close()

	soup = BeautifulSoup(htmlSource, "html.parser")
	x = soup.find_all("div", {"id": "mw-content-text"})

	formatted_child = " "
	
	for child in x:
		formatted_child += child.getText().encode('utf-8') + "\n"
	return formatted_child

def getFlagURL(country):

	page = "https://en.wikipedia.org/wiki/File:Flag_of_" +country+".svg"
	
	urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', page)
	print urls
	return urls


def splitIntoSentences(text):
	# Dzielę całość tekstu na zdania
	zdania = re.split(r'(?<!\w\. \w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|\[[0-9]{2}\]|\[[0-9]{3}\]|\[[0-9]{2}\]\[[0-9]{2}\]|\[[0-9]{3}\]\[[0-9]{3}\])(?=[A-Z]|\n|\s)', text)
	return zdania

def getTagInfo(tag,All):
	Tab = []
	for zdanie in All:
		if (zdanie.find(" " +tag+ " ") !=-1):
			Tab.append(zdanie)

	# 3. Wyświetlam wynik, w ładny i przejrzysty sposób:
	licznik=0
	print "Pasujace zdania:"

	for trafienie in Tab:
		# dla kazdego z trafionych zdań (w których znaleziono taga)
		licznik += 1 # zwiększam o 1, żeby wyświetlanie miało charakter listy od 1...itp
		print licznik, ". ", trafienie
		# np. 1. Przykładowe zdanie w którym jest tag ,"," oznacza pisanie w jednej linii

def databaseCheck(client, countryName):

	#http://api.mongodb.org/python/current/tutorial.html
	# wybieram bazę
	db = client['test-database']

	# decyzja, czy czytać z bazy czy z internetu
	if db.mytable.find_one({"country" : countryName}):
		# jeśli znajdzie w bazie to wczytaj
		print "Znaleziono w bazie, wczytuję:"
		record = db.mytable.find_one({"country" : countryName})
		return record["info"]
	else:
		print "Nie znaleziono w bazie, pobieram z sieci:"
		info = getCountryInfo(countryName)
		jsonInput = {	"country" : countryName,
						"info" : info}
		db.mytable.insert_one(jsonInput)
		print "Zapisano do bazy"
		return jsonInput["info"]

#http://www.python.rk.edu.pl/w/p/tornado-framework-z-obsluga-asynchronicznych-zadan/
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

				info = databaseCheck(client, country)
				zdania = splitIntoSentences(info)
				getTagInfo(zdania)
#			print 'Country: ' + country 
			
				if tagFound:
					tag = tagFound.group(1)
				print 'TAG: ' + tag 
			
			self.write(data_json)
			#print (data_json)
		except Exception, e:
			self.write(json.dumps({'status': 'fail', 'error': "Error occured:\n%s" % traceback.format_exc()}))


# mapowanie URLi
application = tornado.web.Application([(r"/", MainHandler),], debug=True)	


if __name__ == "__main__":
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	tornado.ioloop.IOLoop.instance().start()



#info = databaseCheck(client, country)
#zdania = splitIntoSentences(info)
#getTagInfo(zdania)
getFlagURL(country)

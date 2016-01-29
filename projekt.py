#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient
from sgmllib import SGMLParser
#import sgmllib

country = raw_input("Enter the country: ")
tag = raw_input("Enter the tag: ")


def getCountry(country):
	page = urllib2.urlopen("http://en.wikipedia.org/wiki/" +country)
	htmlSource = page.read()
	page.close()

	soup = BeautifulSoup(htmlSource, "html.parser")
	x = soup.select('div#mw-content-text > p')

	formatted_child = " "
	
	for child in x:
		formatted_child += child.getText().encode('utf-8') + "\n"
	return formatted_child

def splitIntoSentences(text):
	# Dzielę całość tekstu na zdania
	zdania = re.split(r'(?<!\w\. \w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|\[[0-9]{2}\]|\[[0-9]{3}\]|\[[0-9]{2}\]\[[0-9]{2}\]|\[[0-9]{3}\]\[[0-9]{3}\])(?=[A-Z]|\n|\s)', text)
	return zdania

def getTag(All):
	Tab = []
	for zdanie in All:
		if (zdanie.search(" " +tag+ " ") !=-1):
			Tab.append(zdanie)

	# 3. Wyświetlam wynik, w ładny i przejrzysty sposób:
	licznik=0
	print "Pasujace zdania:"

	for trafienie in Tab:
		# dla kazdego z trafionych zdań (w których znaleziono taga)
		licznik += 1 # zwiększam o 1, żeby wyświetlanie miało charakter listy od 1...itp
		print licznik, ". ", trafienie
		# np. 1. Przykładowe zdanie w którym jest tag ,"," oznacza pisanie w jednej linii




client = MongoClient()

info = databaseCheck(client, country)
zdania = splitIntoSentences(info)
findTag(zdania)
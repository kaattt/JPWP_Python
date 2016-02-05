#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests


data = {'address': 'localhost',
        'port': '8888',
        'type': 'text',
        'content': 'country(Poland);tag(Sea)' 
        }
r = requests.post("http://localhost:8888", json=data)
print(r.text)
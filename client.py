import requests
from pprint import pprint

print("Print 'Hello World'")
r = requests.post(url="http://localhost:8080/control", json=[{"command": "text", "data": {"text": "Hello World"}}])
pprint(r.json())

print('Print "Hello World" but larger')
r = requests.post(url="http://localhost:8080/control", json=[{"command": "text", "data": {"text": "Hello World", "size": 4}}])
pprint(r.json())

print('Print two sizes of text on one line')
r = requests.post(url="http://localhost:8080/control", json=[{"command": "text", "data": {"text": "Hello World", "size": 4, "newline": False}}, {"command": "text", "data": {"text": "Hello World", "size": 2}}])
pprint(r.json())

print('Print a qr code that points to example.com')
r = requests.post(url="http://localhost:8080/control", json=[{"command": "qr", "data": {"text": "https://example.com"}}])
pprint(r.json())

print('Print a local image')
r = requests.post(url="http://localhost:8080/control", json=[{"command": "image", "data": {"image": "logo"}}])
pprint(r.json())

print('Print a remote image')
r = requests.post(url="http://localhost:8080/control", json=[{"command": "image", "data": {"image": "https://example.com/logo.png"}}])
pprint(r.json())

print('Cut the paper')
r = requests.post(url="http://localhost:8080/control", json=[{"command": "cut"}])


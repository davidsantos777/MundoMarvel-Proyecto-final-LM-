#_*_ coding: utf-8 _*_

from flask import Flask, render_template, request
import hashlib
import requests
import os
import json

public = '5404f8cbf841577db6f94fb3a3098d51'
private = 'a21215a318c6fb1eeb9e5763e08a9c7352317055'
ts = '1'

app = Flask(__name__)
port = os.environ['PORT']

hash = hashlib.md5((ts + private + public).encode()).hexdigest()

base = "https://gateway.marvel.com/v1/public/"

@app.route('/')
def inicio():
  return render_template('index.html')

@app.route('/busqueda', methods = ["get", "post"])
def busqueda():
  if request.method == "GET":
    return render_template('index.html')
  else:
    lista = []
    nombre = request.form.get("datos")
    tipo = request.form.get("tipo")
    if tipo == "comics":
      payload = {'apikey': public,'ts': ts,'hash': hash,'title': nombre}
      r = requests.get(base + 'comics', params= payload)
      if r.status_code == 200:
        results = r.json()
        for i in results['data']['results']:
          lista.append({'Id': i["id"], 'Titulo': i['title'], 'Sinopsis': i['description']})
    elif tipo == "eventos":
      payload = {'apikey': public,'ts': ts,'hash': hash,'title': nombre}
      r = requests.get(base + 'comics', params= payload)
      if r.status_code == 200:
        results = r.json()
        for i in results['data']['results']:
          lista.append({'Id': i["id"], 'Titulo': i['title'], 'Sinopsis': i['description']})
    return render_template('index.html', datos = lista)

app.run('0.0.0.0', int(port), debug = True)

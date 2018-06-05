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

hash = hashlib.md5((ts + private + public).encode()).hexdigest()

base = "https://gateway.marvel.com/v1/public/"

@app.route('/')
def inicio():
  return render_template('index.html')

@app.route('/busqueda')
def busqueda():
  return render_template('landing.html')

@app.route('/busqueda_personalizada', methods = ["get", "post"])
def busqueda_personalizada():
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
      r = requests.get(base + 'events', params= payload)
      if r.status_code == 200:
        results = r.json()
        for i in results['data']['results']:
          lista.append({'Id': i["id"], 'Titulo': i['title'], 'Sinopsis': i['description']})

    elif tipo == "personajes":
      payload = {'apikey': public,'ts': ts,'hash': hash,'name': nombre}
      r = requests.get(base + 'characters', params= payload)
      if r.status_code == 200:
        results = r.json()
        for i in results['data']['results']:
          lista.append({'Id': i["id"], 'Nombre': i['name'], 'Biografía': i['description']})

    elif tipo == "creadores":
      payload = {'apikey': public,'ts': ts,'hash': hash,'firstName': nombre}
      r = requests.get(base + 'creators', params= payload)
      if r.status_code == 200:
        results = r.json()
        for i in results['data']['results']:
          lista.append({'Id': i["id"], 'Nombre': i['firstName'], 'Sinopsis': i['description']})

    elif tipo == "series":
      payload = {'apikey': public,'ts': ts,'hash': hash,'title': nombre}
      r = requests.get(base + 'series', params= payload)
      if r.status_code == 200:
        results = r.json()
        for i in results['data']['results']:
          lista.append({'Id': i["id"], 'Titulo': i['title'], 'Sinopsis': i['description']})
          
    elif tipo == "historias":
      payload = {'apikey': public,'ts': ts,'hash': hash,'title': nombre}
      r = requests.get(base + 'stories', params= payload)
      if r.status_code == 200:
        results = r.json()
        for i in results['data']['results']:
          lista.append({'Id': i["id"], 'Titulo': i['title'], 'Sinopsis': i['description']})
    return render_template('landing.html', datos = lista)

app.run()
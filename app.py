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

base_2 = "http://comicvine.com/api/search/"   

api_key = '1ab596554f32d6f88221fe969d1a8ca3f67374d1'

@app.route('/')
def inicio():
  return render_template('index.html')


@app.route('/busqueda_comics', methods = ["get", "post"])
def busqueda_comics():
  if request.method == "GET":
    return render_template('busqueda_comics.html')
  else:
    lista = []
    nombre = request.form.get("datos")
    payload = {'apikey': public,'ts': ts,'hash': hash,'title': nombre}
    r = requests.get(base + 'comics', params= payload)
    if r.status_code == 200:
      results = r.json()
      for i in results['data']['results']:
        lista.append({'Id': i["id"], 'Titulo': i['title'], 'Sinopsis': i['description']})

    return render_template('busqueda_comics.html', datos = lista)


@app.route('/resultados_comics/<id>', methods = ["get", "post"])
def resultados_comics(id):
  lista_resultadoc = []
  payload = {'apikey': public,'ts': ts,'hash': hash}
  r = requests.get(base + 'comics/' + id, params= payload)
  if r.status_code == 200:
    results = r.json()
    for i in results['data']['results']:
      lista_resultadoc.append({'Titulo': i['title'],'Sinopsis': i['description'], 'Serie': i['series']['name']})

  return render_template('resultados_comics.html', datos = lista_resultadoc)


@app.route('/busqueda_personajes', methods = ["get", "post"])
def busqueda_personajes():
  if request.method == "GET":
    return render_template('busqueda_personajes.html')
  else:
    lista_2 = []
    lista_img = []
    indicador = False
    nombre_2 = request.form.get("datos")
    nombre_real = request.form.get("datos2")
    payload_2 = {'apikey': public,'ts': ts,'hash': hash,'name': nombre_2}
    payload_img = {'api_key': api_key, 'format': 'json','query': nombre_2}
    r = requests.get(base + 'characters', params= payload_2)
    headers = {'User-Agent': 'Mi aplicación'}
    r_img = requests.get(base_2, params= payload_img, headers = headers)
    if r.status_code == 200 and r_img.status_code == 200:
      results = r.json()
      results_img = r_img.json()
      for i in results['data']['results']:
        if i['description'] == "":
          indicador = False
        else:  
          indicador = True
          
        if indicador == True:
          lista_2.append({'Nombre': i['name'],'Biografia': i['description']})
        else:
          lista_2.append({'Nombre': i['name'],'Biografia': "No hay biografía disponible"})

      for i in results_img['results']:  
        if 'publisher' not in i or i['publisher']['name'] == "Marvel":
          lista_img.append({'Imagen': i['image']['medium_url']})

    return render_template('busqueda_personajes.html', datos = lista_2, datos2 = lista_img)


@app.route('/personajes_relacionados/<nombre>', methods = ["get", "post"])
def personajes_relacionados(nombre):
  lista_personajes = []
  lista_img = []
  payload = {'apikey': public,'ts': ts,'hash': hash, 'name': nombre}
  payload_img = {'api_key': api_key, 'format': 'json','query': nombre}
  headers = {'User-Agent': 'Mi aplicación'}
  r = requests.get(base + 'characters', params= payload)
  r_img = requests.get(base_2, params= payload_img, headers = headers)
  if r.status_code == 200 and r_img.status_code == 200:
    results = r.json()
    results_img = r_img.json()
    for i in results['data']['results']:
      lista_personajes.append({'Nombre': i['name'],'Biografia': i['description']})
    
    for i in results_img['results']:  
        if 'publisher' not in i or i['publisher']['name'] == "Marvel":
          lista_img.append({'Imagen': i['image']['medium_url']})

  return render_template('personajes_relacionados.html', datos = lista_personajes, datos2 = lista_img)


@app.route('/busqueda_eventos', methods = ["get", "post"])
def busqueda_eventos():
  if request.method == "GET":
    return render_template('busqueda_eventos.html')
  else:
    lista_3 = []
    lista_sig_ant = []
    lista_creadores = []
    lista_pj = []
    lista_historias = []
    lista_comics = []
    lista_series = []
    nombre_3 = request.form.get("datos")
    payload_3 = {'apikey': public,'ts': ts,'hash': hash,'name': nombre_3}
    r = requests.get(base + 'events', params= payload_3)
    if r.status_code == 200:
      results = r.json()
      for i in results['data']['results']:
        lista_3.append({'Titulo': i['title'], 'Sinopsis': i['description'], 'Comienzo': i['start'], 'Finalizacion': i['end']})

      for i in results['data']['results']:
        lista_sig_ant.append({'Siguiente': i['next']['name'], 'Anterior': i['previous']['name']})

      for i in results['data']['results'][0]['creators']['items']:
        lista_creadores.append({'Creador': i['name'], 'Rol': i['role']})

      for i in results['data']['results'][0]['characters']['items']:
        lista_pj.append({'Personaje': i['name']})

      for i in results['data']['results'][0]['stories']['items']:
        lista_historias.append({'Historia': i['name']})

      for i in results['data']['results'][0]['comics']['items']:
        lista_comics.append({'Comics': i['name']})

      for i in results['data']['results'][0]['series']['items']:
        lista_series.append({'Series': i['name']})

    return render_template('busqueda_eventos.html', datos = lista_3, datos2 = lista_creadores, datos3 = lista_pj, datos4 = lista_historias, datos5 = lista_comics, datos6 = lista_series, datos7 = lista_sig_ant)

@app.route('/eventos_relacionados/<nombre>', methods = ["get", "post"])
def eventos_relacionados(nombre):
  lista_eventos = []
  lista_sig_ant = []
  lista_creadores = []
  lista_pj = []
  lista_historias = []
  lista_comics = []
  lista_series = []
  payload = {'apikey': public,'ts': ts,'hash': hash, 'name': nombre}
  r = requests.get(base + 'events', params= payload)
  if r.status_code == 200:
    results = r.json()
    for i in results['data']['results']:
      lista_eventos.append({'Titulo': i['title'], 'Sinopsis': i['description'], 'Comienzo': i['start'], 'Finalizacion': i['end']})

    for i in results['data']['results']:
      lista_sig_ant.append({'Siguiente': i['next']['name'], 'Anterior': i['previous']['name']})

    for i in results['data']['results'][0]['creators']['items']:
      lista_creadores.append({'Creador': i['name'], 'Rol': i['role']})

    for i in results['data']['results'][0]['characters']['items']:
      lista_pj.append({'Personaje': i['name']})

    for i in results['data']['results'][0]['stories']['items']:
      lista_historias.append({'Historia': i['name']})

    for i in results['data']['results'][0]['comics']['items']:
      lista_comics.append({'Comics': i['name']})

    for i in results['data']['results'][0]['series']['items']:
      lista_series.append({'Series': i['name']})


  return render_template('eventos_relacionados.html', datos = lista_eventos, datos2 = lista_creadores, datos3 = lista_pj, datos4 = lista_historias, datos5 = lista_comics, datos6 = lista_series, datos7 = lista_sig_ant)


@app.route('/busqueda_creadores', methods = ["get", "post"])
def busqueda_creadores():
  if request.method == "GET":
    return render_template('busqueda_creadores.html')
  else:
    lista_4 = []
    nombre_4 = request.form.get("datos")
    payload_4 = {'apikey': public,'ts': ts,'hash': hash,'firstName': nombre_4}
    r = requests.get(base + 'creators', params= payload_4)
    if r.status_code == 200:
      results = r.json()
      for i in results['data']['results']:
        lista_4.append({'Nombre': i['fullName']})
    return render_template('busqueda_creadores.html', datos = lista_4)


@app.route('/busqueda_series', methods = ["get", "post"])
def busqueda_series():
  if request.method == "GET":
    return render_template('busqueda_series.html')
  else:
    lista_5 = []
    nombre_5 = request.form.get("datos")
    payload_5 = {'apikey': public,'ts': ts,'hash': hash,'title': nombre_5}
    r = requests.get(base + 'series', params= payload_5)
    if r.status_code == 200:
      results = r.json()
      for i in results['data']['results']:
        lista_5.append({'Titulo': i['title'], 'Sinopsis': i['description']})

    return render_template('busqueda_series.html', datos = lista_5)


@app.route('/busqueda_historias', methods = ["get", "post"])
def busqueda_historias():
  if request.method == "GET":
    return render_template('busqueda_historias.html')
  else:
    lista_6 = []
    nombre_6 = request.form.get("datos")
    name = nombre_6
    payload_6 = {'action': 'parse', 'page': nombre_6,'prop': 'text', 'format': 'json', 'callback': '?'}
    r = requests.get(base_wiki, params= payload_6)

    if r.status_code == 200:
      results = r.json()
    

    print (lista_6)
    return render_template('busqueda_historias.html', datos = lista_6)

app.run()
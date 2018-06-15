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
    payload = {'apikey': public,'ts': ts,'hash': hash,'title': nombre.replace(' ', '%20')}
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
      lista_resultadoc.append({'Id': i["id"], 'Titulo': i['title'], 'Sinopsis': i['description'], 'Serie': i['series']['name']})

  return render_template('resultados_comics.html', datos = lista_resultadoc)


@app.route('/series_relacionadas/<nombre>', methods = ["get", "post"])
def series_relacionadas(nombre):
  lista_series = []
  payload = {'apikey': public,'ts': ts,'hash': hash, 'title': nombre}
  r = requests.get(base + 'series', params= payload)
  if r.status_code == 200:
    results = r.json()
    for i in results['data']['results']:
      lista_series.append({'Id': i["id"], 'Titulo': i['title'],'Sinopsis': i['description'], 'Creador': i['creators']['items'], 'Personaje': i['characters']['items'], 'Historia': i['stories']['items'], 'Comic': i['comics']['items'], 'Evento': i['events']['items']})

  return render_template('series_relacionadas.html', datos = lista_series)


@app.route('/busqueda_personajes', methods = ["get", "post"])
def busqueda_personajes():
  if request.method == "GET":
    return render_template('busqueda_personajes.html')

  else:
    lista_2 = []
    lista_img = []
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
        lista_2.append({'Id': i["id"], 'Nombre': i['name'],'Biografia': i['description']})

      for i in results_img['results']: 
        if 'publisher' not in i or i['publisher']['name'] == "Marvel":
          lista_img.append({'Imagen': i['image']['medium_url']})

    return render_template('busqueda_personajes.html', datos = lista_2, datos2 = lista_img)


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
    payload_3 = {'apikey': public,'ts': ts,'hash': hash,'name': nombre_3.replace(' ', '%20')}
    r = requests.get(base + 'events', params= payload_3)
    if r.status_code == 200:
      results = r.json()

      for i in results['data']['results']:
        lista_3.append({'Id': i["id"], 'Titulo': i['title'], 'Sinopsis': i['description'], 'Comienzo': i['start'], 'Finalizacion': i['end']})

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
      lista_eventos.append({'Id': i["id"], 'Titulo': i['title'], 'Sinopsis': i['description'], 'Comienzo': i['start'], 'Finalizacion': i['end']})

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
      lista_personajes.append({'Id': i["id"], 'Nombre': i['name'],'Biografia': i['description']})
    
    for i in results_img['results']: 
        if 'publisher' not in i or i['publisher']['name'] == "Marvel":
          lista_img.append({'Imagen': i['image']['medium_url']})

  return render_template('personajes_relacionados.html', datos = lista_personajes, datos2 = lista_img)


@app.route('/comics_relacionados/<nombre>', methods = ["get", "post"])
def comics_relacionados(nombre):
  lista_comics = []
  payload = {'apikey': public,'ts': ts,'hash': hash, 'title': nombre}
  r = requests.get(base + 'comics', params= payload)
  if r.status_code == 200:
    results = r.json()
    for i in results['data']['results']:
      lista_comics.append({'Id': i["id"], 'Titulo': i['title'],'Sinopsis': i['description'], 'Serie': i['series']['name']})

  return render_template('comics_relacionados.html', datos = lista_comics)


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
        lista_4.append({'Id': i["id"], 'Nombre': i['fullName'],'Comics': i['comics']['items'], 'Series': i['series']['items'], 'Historias': i['stories']['items'], 'Eventos': i['events']['items']})

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
        lista_5.append({'Id': i["id"], 'Titulo': i['title'],'Sinopsis': i['description'], 'Creador': i['creators']['items'], 'Personaje': i['characters']['items'], 'Historia': i['stories']['items'], 'Comic': i['comics']['items'], 'Evento': i['events']['items']})

    return render_template('busqueda_series.html', datos = lista_5)


@app.route('/busqueda_historias', methods = ["get", "post"])
def busqueda_historias():
  if request.method == "GET":
    return render_template('busqueda_historias.html')

  else:
    lista_series = []
    lista_comics = []
    lista_pj = []
    lista_eventos = []
    lista_creadores = []

    ID = request.form.get("datos")

    payload_series = {'apikey': public,'ts': ts,'hash': hash,'series': ID}
    r_series = requests.get(base + 'stories', params= payload_series)

    payload_comics = {'apikey': public,'ts': ts,'hash': hash,'comics': ID}
    r_comics = requests.get(base + 'stories', params= payload_comics)

    payload_pj = {'apikey': public,'ts': ts,'hash': hash,'characters': ID}
    r_pj = requests.get(base + 'stories', params= payload_pj)

    payload_eventos = {'apikey': public,'ts': ts,'hash': hash,'events': ID}
    r_eventos = requests.get(base + 'stories', params= payload_eventos)

    payload_creadores = {'apikey': public,'ts': ts,'hash': hash,'creators': ID}
    r_creadores = requests.get(base + 'stories', params= payload_creadores)

    if r_series.status_code == 200 or r_comics.status_code == 200 or r_pj.status_code == 200 or r_eventos.status_code == 200 or r_creadores.status_code == 200:     
      results_series = r_series.json()
      results_comics = r_comics.json()
      results_pj = r_pj.json()
      results_eventos = r_eventos.json()
      results_creadores = r_creadores.json()
      for i in results_series['data']['results']:
        lista_series.append({'Serie': i['series']['items'], 'Comic': i['comics']['items'], 'Personaje': i['characters']['items'], 'Evento': i['events']['items'], 'Creador': i['creators']['items']})

      for i in results_comics['data']['results']:        
        lista_comics.append({'Comic': i['comics']['items'], 'Serie': i['series']['items'], 'Personaje': i['characters']['items'], 'Evento': i['events']['items'], 'Creador': i['creators']['items']})

      for i in results_pj['data']['results']:
        lista_pj.append({'Personaje': i['characters']['items'], 'Serie': i['series']['items'], 'Comic': i['comics']['items'], 'Evento': i['events']['items'], 'Creador': i['creators']['items']})

      for i in results_eventos['data']['results']:
        lista_eventos.append({'Evento': i['events']['items'], 'Serie': i['series']['items'], 'Comic': i['comics']['items'], 'Personaje': i['characters']['items'], 'Creador': i['creators']['items']})
   
      for i in results_creadores['data']['results']:
        lista_creadores.append({'Creador': i['creators']['items'], 'Serie': i['series']['items'], 'Comic': i['comics']['items'], 'Personaje': i['characters']['items'], 'Evento': i['events']['items']})

    return render_template('busqueda_historias.html', datos = lista_series, datos2 = lista_comics, datos3 = lista_pj, datos4 = lista_eventos, datos5 = lista_creadores)

port=os.environ["PORT"]

app.run('0.0.0.0',int(port), debug=True)

# OPEN WEATHER

## Api desenvolvida para retornar a previsão do tempo dos proximos 5 dias com 3 horas de intervalo entre cada dado. Esse projeto é apenas um estudo, portanto há muita coisa para se melhorar!

![Badge](https://img.shields.io/badge/Python-v3.11-blue?style=plastic&logo=python)
![Badge](https://img.shields.io/badge/Docker-v3.8-blue?style=plastic&logo=docker)
![Badge](https://img.shields.io/badge/Fastapi-v0.92.0-yellowgreen?style=plastic&logo=fastapi)
![Badge](https://img.shields.io/badge/MongoDB--green?style=plastic&logo=mongoDB)

# ✏️ Sumário

### Criando Ambiente Local

- [Instalando Docker](#--instalando-docker)
- [Subindo os Containers](#--subindo-os-containers)

### Fazendo a Requisição

- [Fazendo a Requisição](#🌐-Fazendo-a-Requisição)
  - [/api/get_forecast](#🌥️-/api/get_forecast)
  - [/api/check_day](#🌦️-/api/check_day)

# 🛠️ Criando Ambiente Local

## 🐋 Instalando Docker

---

Utilizamos localmente um docker para API e Banco de Dados.

Para instalar o docker-compose:

```bash
# Instalar o docker-compose
$ apt-get install docker-compose
```

Caso o Docker não seja instalado como dependencia do docker-compose por algum motivo, instale o docker

```bash
#instalando docker
$ apt-get update -y && apt-get install docker
```

## 🐳 Subindo os Containers

---

Para subir os containers basta rodar o comando:

```bash
# Acrescente a tag --build se precisar
$ docker-compose up -d --build
```

# 🌐 Fazendo a Requisição

A API só tem endpoints GET, portando você consegue fazer do seu navegador ou do proprio swagger.
Para acessar o docs do fastapi e ver os parametros necessarios, entrem em:

```
localhost:8000/docs
```

### 🌥️ /api/get_forecast

Vai retornar um novo dado da api do open weather e adiciona-lo no nosso banco.
Caso lat e lon sejam passados, eles serão os parametros usados para a busca.

```
http://localhost:8000/api/get_forecast?city_name=Belo%20Horizonte&country_code=BRA&units=metric
```

- city_name = Nome da cidade que deseja retornar | Ex: Rio de Janeiro
- country_code = Codigo ISO 3166 do país | Ex: BRA
- units = unidade de medida do retorno | metric, imperial ou standard
  - metric para celsius (C°)
  - imperial para fahrenheit (F°)
  - standard para kelvin (kelvin)
- lat = latitude da cidade | opcional
- lon = longitude da cidade | opcional

### 🌦️ /api/check_day

Vai retornar as informações mais atuais que ja temos no banco de dados para o dia e cidade explicitada.

- day = data que gostaria de buscar no formato dd/mm/aaaa | ex: '01/04/2023'

- city = nome da cidade que deseja retornar | ex: Rio de Janeiro

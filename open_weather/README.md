# OPEN WEATHER

## Api desenvolvida para retornar a previsão do tempo dos proximos 5 dias com 3 horas de intervalo entre cada dado. Esse projeto é apenas um estudo, portanto há muita coisa para se melhorar!

![Badge](https://img.shields.io/badge/Python-v3.11-blue?style=plastic&logo=python)
![Badge](https://img.shields.io/badge/Docker-v3.8-blue?style=plastic&logo=docker)
![Badge](https://img.shields.io/badge/Fastapi-v0.92.0-yellowgreen?style=plastic&logo=fastapi)
![Badge](https://img.shields.io/badge/MongoDB-15.0-green?style=plastic&logo=mongoDB)

# ✏️ Sumário

### Criando Ambiente Local

- [Instalando Docker](#--instalando-docker)
- [Subindo os Containers](#--subindo-os-containers)

### Padronização de Commits

- [Padrão de Commits](#-padrão-de-commits)
  - [Conventional Commits](#--conventional-commits)
  - [Conventional Commits Types](#--conventional-commits-types-)
  - [Conventional Commits BREAKING CHANGE](#--conventional-commits-breaking-change-)
  - [Extensão VSCODE](#--extensão-do-vscode)

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

A requisição a ser feita é um GET, portando você conseg

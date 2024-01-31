import requests
import json

# Definiere die erforderlichen Variablen
variables = {
    "email": "<email>",
    "password": "<password>",
    "sessionid": "",
    "token": "",
    "pod": "<pod>",
    "url": "<url>",
    "uuid": ""
}

# Funktion für den Login
def login():
    url = "https://{}/enduser-mobile-web/enduserAPI/login".format(variables["url"])
    headers = {"Content-Type": "application/json"}
    data = {
        "userId": variables["email"],
        "userPassword": variables["password"]
    }
    response = requests.post(url, headers=headers, json=data)
    variables["sessionid"] = response.json()["roles"][0]["name"]

# Funktion zum Generieren eines Tokens
def generate_token():
    url = "https://{}/enduser-mobile-web/enduserAPI/config/{}/{}/local/tokens/generate".format(variables["url"], variables["pod"], variables["sessionid"])
    headers = {
        "Content-Type": "application/json",
        "Cookie": "JSESSIONID={}".format(variables["sessionid"])
    }
    response = requests.get(url, headers=headers)
    variables["token"] = response.json()["token"]

# Funktion zum Aktivieren eines Tokens
def activate_token():
    url = "https://{}/enduser-mobile-web/enduserAPI/config/{}/{}/local/tokens".format(variables["url"], variables["pod"], variables["sessionid"])
    headers = {
        "Content-Type": "application/json",
        "Cookie": "JSESSIONID={}".format(variables["sessionid"])
    }
    data = {
        "label": "Toto token",
        "token": variables["token"],
        "scope": "devmode"
    }
    response = requests.post(url, headers=headers, json=data)

# Funktion zum Abrufen verfügbarer Tokens
def get_tokens():
    url = "https://{}/enduser-mobile-web/enduserAPI/config/{}/{}/local/tokens/devmode".format(variables["url"], variables["pod"], variables["sessionid"])
    headers = {
        "Content-Type": "application/json",
        "Cookie": "JSESSIONID={}".format(variables["sessionid"])
    }
    response = requests.get(url, headers=headers)
    variables["uuid"] = response.json()[0]["uuid"]

# Funktion zum Löschen eines Tokens
def delete_token():
    url = "https://{}/enduser-mobile-web/enduserAPI/config/{}/{}/local/tokens/{}".format(variables["url"], variables["pod"], variables["sessionid"], variables["uuid"])
    headers = {
        "Content-Type": "application/json",
        "Cookie": "JSESSIONID={}".format(variables["sessionid"])
    }
    response = requests.delete(url, headers=headers)

# Durchführen der Aktionen
login()
generate_token()
activate_token()
get_tokens()
delete_token()

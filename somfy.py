# -*- coding: utf-8 -*-
import requests
import json

# Definiere die erforderlichen Variablen
variables = {
    "email": "YOUR_EMAIL_ADDRESS",
    "password": "YOUR_PASSWORD",
    "sessionid": "",
    "token": "",
    "pod": "YOUR_GATEWAY_PIN",
    "url": "ha101-1.overkiz.com",
    "uuid": ""
}

# Funktion für den Login
def login():
    url = "https://{}/enduser-mobile-web/enduserAPI/login".format(variables["url"])
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "userId": variables["email"],
        "userPassword": variables["password"]
    }
    response = requests.post(url, headers=headers, data=data)

    print("Login response status code:", response.status_code)
    print("Login response text:", response.text)

    if response.status_code == 200:
        # Session-ID extrahieren
        variables["sessionid"] = response.cookies.get("JSESSIONID")
        print("Login successful.")
    else:
        print("Failed to login.")

# Funktion zum Generieren eines Tokens
def generate_token():
    url = "https://{}/enduser-mobile-web/enduserAPI/config/{}/local/tokens/generate".format(variables["url"], variables["pod"])
    headers = {
        "Content-Type": "application/json",
        "Cookie": "JSESSIONID={}".format(variables["sessionid"])
    }
    response = requests.get(url, headers=headers)

    print("Generate token response status code:", response.status_code)
    print("Generate token response text:", response.text)

    if response.status_code == 200:
        variables["token"] = response.json().get("token")
        print("Token generated successfully.")
    else:
        print("Failed to generate token.")

# Funktion zum Aktivieren eines Tokens
def activate_token():
    url = "https://{}/enduser-mobile-web/enduserAPI/config/{}/local/tokens".format(variables["url"], variables["pod"])
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

    print("Activate token response status code:", response.status_code)
    print("Activate token response text:", response.text)

    if response.status_code == 200:
        print("Token activated successfully.")
    else:
        print("Failed to activate token.")

# Funktion zum Abrufen verfügbarer Tokens
def get_tokens():
    url = "https://{}/enduser-mobile-web/enduserAPI/config/{}/local/tokens/devmode".format(variables["url"], variables["pod"])
    headers = {
        "Content-Type": "application/json",
        "Cookie": "JSESSIONID={}".format(variables["sessionid"])
    }
    response = requests.get(url, headers=headers)

    print("Get tokens response status code:", response.status_code)
    print("Get tokens response text:", response.text)

    if response.status_code == 200:
        variables["uuid"] = response.json()[0].get("uuid")
        print("Token UUID retrieved successfully.")
    else:
        print("Failed to retrieve token UUID.")

# Funktion zum Löschen eines Tokens
def delete_token():
    url = "https://{}/enduser-mobile-web/enduserAPI/config/{}/local/tokens/{}".format(variables["url"], variables["pod"], variables["uuid"])
    headers = {
        "Content-Type": "application/json",
        "Cookie": "JSESSIONID={}".format(variables["sessionid"])
    }
    response = requests.delete(url, headers=headers)

    print("Delete token response status code:", response.status_code)
    print("Delete token response text:", response.text)

    if response.status_code == 200:
        print("Token deleted successfully.")
    else:
        print("Failed to delete token.")

# Durchführen der Aktionen
login()
generate_token()
activate_token()
get_tokens()
delete_token()

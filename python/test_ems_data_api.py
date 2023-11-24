#!/usr/bin/env python3

import datetime  # required only for the example payload
import json  # required only for pretty printing the responses
import os  # required only for reading env variables
import requests

from ems_data import get_token, COMPANY_NAME


SERVER: str = os.environ['EMS_SERVER']  # e.g. 'https://test.enersem.it/'
UNIT_ID: int = os.environ['EMS_UNIT_ID']
UNIT_ARKE_KEY: str = os.environ['EMS_UNIT_ARKE_KEY']
COMPANY_NAME: str = os.environ['EMS_COMPANY']


def test_verbose():
    print("################")
    print("Examples of JWT-authenticated API calls to EMS by ENERSEM.")

    print("\n################")
    print("Get the token from the private_key.pem file... ", end='')
    token = get_token(COMPANY_NAME)
    print(f"done: \n{token}")

    print("\n################")
    print("Post new values of a single parameter of an arke... ", end='')
    url = f"{SERVER}api/data/{UNIT_ARKE_KEY}/parameter/electric_energy"
    dt_now = datetime.datetime.now()
    values = [
        {
            "datetime": "2011-11-11T11:11:11",
            "value": "5"
        },
        {
            "datetime": dt_now.isoformat(),
            "value": 424.2
        },
    ]
    r = requests.post(url, json=values, headers={'Authorization': token})
    print(f"done: \n{r}")
    print(json.dumps(r.json(), indent=2))
    assert r.status_code == 201
    assert len(r.json()['messages']) == 0
    assert len(r.json()['content']) == 2

    print("\n################")
    print("Read the updated value... ", end='')
    url = f"{SERVER}api/data/{UNIT_ARKE_KEY}/parameter/electric_energy"
    r = requests.get(url, headers={'Authorization': token})
    print(f"done: \n{r}")
    print(json.dumps(r.json(), indent=2))
    assert r.status_code == 200
    assert len(r.json()['messages']) == 0

    print("\n################")
    print("Get the history to see the other values... ", end='')
    url = f"{SERVER}api/data/{UNIT_ARKE_KEY}/parameter/electric_energy/history"
    r = requests.get(url, headers={'Authorization': token})
    print(f"done: \n{r}")
    print(json.dumps(r.json(), indent=2))
    assert r.status_code == 200
    assert len(r.json()['messages']) == 0

    print("\n################")
    print("Post new values of multiple parameters of an arke... ", end='')
    url = f"{SERVER}api/data/{UNIT_ARKE_KEY}/parameter/"
    dt_now = datetime.datetime.now()
    values = {
        "electric_energy": {
            "datetime": dt_now.isoformat(),
            "value": 424.2
        },
        "heating_energy": {
            "datetime": dt_now.isoformat(),
            "value": 324.2
        },
    }
    r = requests.post(url, json=values, headers={'Authorization': token})
    print(f"done: \n{r}")
    print(json.dumps(r.json(), indent=2))
    assert r.status_code == 201
    assert len(r.json()['messages']) == 0
    assert len(r.json()['content']) == 2

    print("\n################")
    print("Get the updated values... ", end='')
    url = f"{SERVER}api/data/{UNIT_ARKE_KEY}/parameter/"
    r = requests.get(url, headers={'Authorization': token})
    print(f"done: \n{r}")
    print(json.dumps(r.json(), indent=2))
    assert r.status_code == 200
    assert len(r.json()['messages']) == 0

    print("\n################")
    print("Post new values of multiple parameters of multiple arke... ",
          end='')
    url = f"{SERVER}api/data/"
    dt_now = datetime.datetime.now()
    values = [
        {
            "datetime": dt_now.isoformat(),
            "value": 424.2,
            "object_metadata": UNIT_ID,
            "parameter": "electric_energy",
        },
        {
            "object_metadata": UNIT_ID,
            "parameter": "heating_energy",
            "datetime": dt_now.isoformat(),
            "value": 324.2
        },
    ]
    r = requests.post(url, json=values, headers={'Authorization': token})
    print(f"done: \n{r}")
    print(json.dumps(r.json(), indent=2))
    assert r.status_code == 201
    assert len(r.json()['messages']) == 0


if __name__ == '__main__':
    test_verbose()

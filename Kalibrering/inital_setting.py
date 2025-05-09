
def gather_sensor_ids(credentials, token):
    from requests.auth import HTTPBasicAuth
    import requests

    username = "user"
    password = ":".join([credentials, token]) 
    base_url = "https://cowidk.infralogin.com/api/v1/sensor"
    auth = HTTPBasicAuth(username, password)

    years = 2

    # Laver request til Sigicom API server
    response = requests.get(url=base_url, auth=auth, headers={'accept': 'application/json'})
    data = response.json()
    data = [sensor for sensor in data if sensor["type"] == "C22" or sensor["type"] == "V12"]
    sensor_ids = [entry["serial"] for entry in data]

    return sensor_ids, base_url, auth, years
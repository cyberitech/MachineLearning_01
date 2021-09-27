import requests, json
from concurrent.futures import ThreadPoolExecutor

key = "AIzaSyCtHwyX8Vygn6MQNLhFz3P_je0rG11tVdo"
str_end = ",+Australia"

cities = ['Albury', 'BadgerysCreek', 'Cobar', 'CoffsHarbour', 'Moree',
          'Newcastle', 'NorahHead', 'NorfolkIsland', 'Penrith', 'Richmond',
          'Sydney', 'SydneyAirport', 'WaggaWagga', 'Williamtown',
          'Wollongong', 'Canberra', 'Tuggeranong', 'MountGinini', 'Ballarat',
          'Bendigo', 'Sale', 'MelbourneAirport', 'Melbourne', 'Mildura',
          'Nhil', 'Portland', 'Watsonia', 'Dartmoor', 'Brisbane', 'Cairns',
          'GoldCoast', 'Townsville', 'Adelaide', 'MountGambier', 'Nuriootpa',
          'Woomera', 'Albany', 'Witchcliffe', 'PearceRAAF', 'PerthAirport',
          'Perth', 'SalmonGums', 'Walpole', 'Hobart', 'Launceston',
          'AliceSprings', 'Darwin', 'Katherine', 'Uluru']

out_data = {city: {"lat": None, "long": None} for city in cities}

futures = []

for city in cities:
    print(f"processing {city}")
    req_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city + str_end}&key={key}"
    req=requests.get(req_url)
    if req.status_code != 200:
        print(f"Requst failued: {req.status_code}")
        print(req.text)
        continue
    res = json.loads(req.text)

    lat_ne = res['results'][0]["geometry"]["viewport"]["northeast"]["lat"]
    lat_sw = res['results'][0]["geometry"]["viewport"]["southwest"]["lat"]
    long_ne = res['results'][0]["geometry"]["viewport"]["northeast"]["lng"]
    long_sw = res['results'][0]["geometry"]["viewport"]["southwest"]["lng"]
    lat_avg = (lat_ne + lat_sw) / 2
    long_avg = (long_ne + long_sw) / 2
    out_data[city]["lat"] = lat_avg
    out_data[city]["long"] = long_avg
with open("geocoded-cities.json", "w") as f:
    f.write(json.dumps(out_data, indent=4))
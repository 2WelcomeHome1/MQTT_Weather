import requests, json

class get_weather ():
    def __init__(self) -> None:
        self.v_dict, self.i_dict = {}, {}
        self.weather_api_url = 'https://api.data.gov.sg/v1/environment/air-temperature'        
        pass

    def merge_dict(self, d1, d2):
        return {k: tuple(d[k] for d in (d1, d2) if k in d) for k in set(d1.keys()) | set(d2.keys())}
    
    def make_dict(self, merge = False):
        for s_id, d_id in zip(self.station_value, self.stations_info): 
            self.v_dict[s_id['station_id']], self.i_dict[d_id['id']] = s_id['value'], d_id['name']
        if merge: return self.merge_dict(self.v_dict, self.i_dict)
        return self.v_dict
    
    def jsonify(self, data):
            j_temp_data = json.loads(data.text)
            self.status = j_temp_data['api_info']['status']
            self.stations_info = j_temp_data['metadata']['stations']
            self.station_value = j_temp_data['items'][0]['readings']
   
    def get_weather(self, merge):
        temp_data = requests.get(self.weather_api_url)
        if temp_data.status_code == 200:
            self.jsonify(temp_data)
            combine = self.make_dict(merge) # merge = False
            return combine, self.status

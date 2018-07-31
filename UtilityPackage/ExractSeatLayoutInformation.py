from ConfigVars import urls
import requests
import json,random


class ExtractSessionID:

    def hit_v1_json(self):

        headers = {
            'Cache-Control': "no-cache"
        }
        session_url = urls.GET_SESSION_IDS_API.split(",")[1]
        session_method = urls.GET_SESSION_IDS_API.split(",")[0]
        response = requests.request(session_method, session_url, headers=headers)
        json_obj=json.loads(response.text)
        print(json_obj["sessions"][0]["id"])

    def get_seat_avaliable(self, session_id):
        headers = {
            'Cache-Control': "no-cache"
        }
        session_url = urls.GET_SEAT_AVALIABLITY.split(",")[1].format(session_id)
        session_method = urls.GET_SEAT_AVALIABLITY.split(",")[0]
        response = requests.request(session_method, session_url, headers=headers)
        return json.loads(response.text)["availableSeats"][0]

# Retrieves data from the public stash API

import requests
import json
from random import randint
import time
BASE_API_URL = 'http://www.pathofexile.com/api/public-stash-tabs'


class Retriever:
    def retrieve(self, next_id, request_time):
        payload = {}
        payload = {'id': next_id}
        while time.time() <= request_time:
            time.sleep(0.1)
        r = requests.get(BASE_API_URL, params=payload)
        json_data = json.loads(r.text.lower())
        last_id = next_id
        next_id = self._decode_next_id(json_data)
        if next_id == -1:
            # Retry loading
            return self.retrieve(last_id, request_time)
        elif next_id == None:
            return None
        return json_data['stashes']

    def _decode_next_id(self, json_data):
        # Indicates that there is a next page of data to retrieve
        # If not true, the next update has not yet been released
        if 'stashes' not in json_data:
            print('A retriever was rate limited, pausing for 20 seconds..')
            # We requested too fast, chill.
            time.sleep(20)
            return -1
        if len(json_data['stashes']) > 0:
            return json_data['next_change_id']
        else:
            print('Could not yet get next id. Reached end of updates for now.')
            return None

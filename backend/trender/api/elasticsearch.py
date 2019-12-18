import json

import requests


# TODO: currently this class is suitable to load messages 1 by 1 and it
# TODO: significantly slows down the scraping process
# TODO: this should be modified to take in multiple data entries at once
# TODO: like https://github.com/pushshift/telegram/blob/master/elastic.py

class Data:
    def __init__(self, group, subgroup, source, added_date, date, body, metatags):
        self.group = group
        self.subgroup = subgroup
        self.source = source
        self.added_date = added_date
        self.date = date
        self.body = body
        self.metatags = metatags

# Bulk indexing class, hopefully there will be improvements to allow actual bulk indexing
class ES:
    def __init__(self, host, index):
        self._host = host
        self._index = index
        self._headers = {
            "Accept": "application/json",
            "Content-type": "application/json; charset=utf-8",
        }

    def bulk_insert(self, messages, action="index"):
        bulk_str = ""

        if len(messages) == 0:
            return

        for message in messages:
            # bulk_str += '{"%s":{"_index":"%s","_id":"%s"}}\n' % (action, self._index, str(message["id"]))
            bulk_str += '{"%s":{"_index":"%s"}}\n' % (action, self._index)
            bulk_str += json.dumps(message, sort_keys=True, ensure_ascii=False) + "\n"

        r = requests.post(self._host + "/_bulk", data=bulk_str.encode("utf-8"), headers=self._headers)
        content = r.json()

        print("Indexed %d documents <%d>" % (len(messages), r.status_code))

        if r.status_code != 200:
            raise Exception("Elasticsearch error: " + r.text)
        if content["errors"]:
            raise Exception("Elasticsearch error: " + r.text)

def prepare_for_es(data):
    es_record = {
        "group_name": data.group,
        "subgroup_name": data.subgroup,
        "source_name": data.source,
        "added_timestamp": int(data.added_date),
        "created_timestamp": int(data.date),
        "body": data.body,
        "metatags": data.metatags
    }
    return es_record
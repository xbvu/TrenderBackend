import json

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

from trender.config import DefaultConfig

elastic = Elasticsearch()


def query(arguments):

    if not isinstance(arguments, dict):
        raise TypeError
        return
    arguments = arguments.to_dict()
    arguments_list = ["body", "group_name", "subgroup_name", "source_name",
                 "utc_date_before", "utc_date_after", "time_interval"]

    must = []
    if 'search_term' in arguments.keys(): # in ES index it's called body
        arguments['body'] = arguments.pop('search_term')

    for a in arguments.keys():
        # print("{} {}".format(a, arguments[a]))
        if a in arguments_list:
            must.append({"term":{a: arguments[a]}})
    search_index=DefaultConfig.ES_INDEX

    # print(json.dumps({"query": {"bool": {"must": must}}}, indent=4))
    try:
        res = elastic.search(index=search_index, body={"query": {"bool": {"must": must}}})
    except NotFoundError:
        return {}

    # print("Got %d Hits:" % res['hits']['total']['value'])

    return res['hits']['hits']
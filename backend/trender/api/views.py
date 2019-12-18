# -*- coding: utf-8 -*-

import datetime

from flask import Blueprint, request, jsonify
from flask import current_app as app
from flask_restful import Api
from flask_cors import CORS, cross_origin
from sqlalchemy.orm.exc import NoResultFound

from trender.api.elasticsearch import ES, Data, prepare_for_es
from trender.api.models import Group, Subgroup, Source, Entry
from trender.api.search import query
from trender.config import DefaultConfig
from trender.extensions import db

api = Blueprint('api', __name__, url_prefix='/api')
CORS(api)
api_wrap = Api(api)


INDEX_ELASTIC = True
if INDEX_ELASTIC:
    es = ES(
        DefaultConfig.ES_HOST,
        DefaultConfig.ES_INDEX,
     )

@api.route('/input/new_group', methods=['POST'])
@cross_origin()
def new_group():
    arguments = {'name' : '', 'title' : '', 'description' : ''}
    for a in arguments.keys():
        if a in request.form:
            arguments[a] = request.form[a]
        else:
            return "Please specify '%s' argument." % a

    with app.app_context():
        new_group = Group(name=arguments['name'].lower(),
                          title=arguments['title'],
                          description=arguments['description'])
        db.session.add(new_group)
        db.session.commit()

        return "Group '%s' successfully added!" % arguments['name']

@api.route('/input/<group_name>/new_subgroup', methods=['POST'])
@cross_origin()
def new_subgroup(group_name):
    group_name = group_name.lower()
    try:
        group = db.session.query(Group).filter(
            Group.name == group_name).one()
    except NoResultFound:
        return "No group named '{}' found.".format(group_name)
    arguments = {'name':'', 'title':'', 'description':''}
    for a in arguments.keys():
        if a in request.form:
            arguments[a] = request.form[a]
        else:
            return "Please specify '%s' argument." % a

        name = db.session.query(Subgroup).filter(
            Subgroup.name == arguments['name']).first()
        if name is not None:
            return("Subgroup named '%s' already exists." % arguments['name'])
    with app.app_context():
        s = Subgroup(name=arguments['name'].lower(),
                    title=arguments['title'],
                    description=arguments['description'])
        group.subgroups.extend([s])
        db.session.add(group)
        db.session.commit()
        return "Source '%s' successfully added!" % arguments['name']

@api.route('/input/<subgroup_name>/new_source', methods=['POST'])
@cross_origin()
def new_source(subgroup_name):
    subgroup_name = subgroup_name.lower()
    try:
        subgroup = db.session.query(Subgroup).filter(
            Subgroup.name == subgroup_name).one()
    except NoResultFound:
        return "No subgroup named '{}' found.".format(subgroup_name)
    arguments = {'name':'', 'title':'', 'description':''}
    for a in arguments.keys():
        if a in request.form:
            arguments[a] = request.form[a]
        else:
            return "Please specify '%s' argument." % a

        name = db.session.query(Source).filter(
            Source.name == arguments['name']).first()
        if name is not None:
            return("Source named '%s' already exists." % arguments['name'])
    with app.app_context():
        r1 = Source(name=arguments['name'].lower(),
                    title=arguments['title'],
                    description=arguments['description'])
        subgroup.sources.extend([r1])
        db.session.add(subgroup)
        db.session.commit()
        return "Source '%s' successfully added!" % arguments['name']
    
@api.route('/input/<source_name>/new_entry', methods=['POST'])
@cross_origin()
def new_entry(source_name):
    source_name = source_name.lower()
    try:
        source = db.session.query(Source).filter(
            Source.name == source_name).one()

        # TODO: make it search by id and not by string name for more efficiency
        subgroup_id = source.subgroup_id
        subgroup = db.session.query(Subgroup).filter(
            Subgroup.id == subgroup_id).one()
        subgroup_name = subgroup.name
        group_id = subgroup.group_id
        group = db.session.query(Group).filter(
            Group.id == group_id).one()
        group_name = group.name

    except NoResultFound:
        return "No source named '{}' found.".format(source_name)
    arguments = {'timestamp':'', 'body':'', 'metatags':''}
    for a in arguments.keys():
        if a in request.form:
            arguments[a] = request.form[a]
        else:
            return "Please specify '%s' argument." % a

        # no duplicate checking, since it would take too much resources
    with app.app_context():
        r1 = Entry(date=datetime.datetime.fromtimestamp(
            float(arguments['timestamp'])),
            body=arguments['body'],
            metatags=arguments['metatags'])
        source.entries.extend([r1])
        db.session.add(source)
        db.session.commit()

        if INDEX_ELASTIC:
            d = Data(group_name, subgroup_name, source_name, datetime.datetime.utcnow().timestamp(),
                     float(arguments['timestamp']), arguments['body'].lower(), arguments['metatags'])
            d_prepared = prepare_for_es(d)

            # TODO: improve indexing speeds by actually implementing bulk indexing
            # TODO: decide whether it's worth to index single entries using the ES library
            es.bulk_insert([d_prepared])
        return "Entry '%s' successfully added!" % r1.id


@api.route('/search', methods=['POST'])
@cross_origin()
def search():
    search_scopes = ['source', 'subgroup', 'group']

    if "search_term" not in request.form.keys():
        return jsonify({"error":"search_term not specified"})

    q = query(request.form)
    hits = []
    for hit in q:

        search_scope = "null"
        for scope in search_scopes:
            if scope in hit.keys():
                search_scope = scope
            pass
        hits.append({"search_term": request.form["search_term"],
                    "search_scope": search_scope, "timestamp": hit["_source"]["created_timestamp"]})

    return jsonify(hits)
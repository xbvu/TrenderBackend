# -*- coding: utf-8 -*-

import datetime
import os

from flask import Flask, Blueprint, request, jsonify
from flask_restful import Api, Resource
from sqlalchemy.orm.exc import NoResultFound
from flask_sqlalchemy import SQLAlchemy

from trender.api.models import Group, Subgroup, Source, Entry
from trender.extensions import db
from flask import current_app as app

api = Blueprint('api', __name__, url_prefix='/api')
api_wrap = Api(api)


@api.route('/input/new_group', methods=['POST'])
def new_group():
    arguments = {'name':'', 'title':'', 'description':''}
    for a in arguments.keys():
        if a in request.form:
            arguments[a] = request.form[a]
        else:
            return "Please specify '%s' argument." % a
            break
    with app.app_context():
        new_group = Group(name=arguments['name'],
                          title=arguments['title'],
                          description=arguments['description'])
        db.session.add(new_group)
        db.session.commit()

        return "Group '%s' successfully added!" % arguments['name']

@api.route('/input/<group_name>/new_subgroup', methods=['POST'])
def new_subgroup(group_name):
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
            break
        name = db.session.query(Subgroup).filter(
            Subgroup.name == arguments['name']).first()
        if name is not None:
            return("Subgroup named '%s' already exists." % arguments['name'])
    with app.app_context():
        s = Subgroup(name=arguments['name'],
                    title=arguments['title'],
                    description=arguments['description'])
        group.subgroups.extend([s])
        db.session.add(group)
        db.session.commit()
        return "Source '%s' successfully added!" % arguments['name']

@api.route('/input/<subgroup_name>/new_source', methods=['POST'])
def new_source(subgroup_name):
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
            break
        name = db.session.query(Source).filter(
            Source.name == arguments['name']).first()
        if name is not None:
            return("Source named '%s' already exists." % arguments['name'])
    with app.app_context():
        r1 = Source(name=arguments['name'],
                    title=arguments['title'],
                    description=arguments['description'])
        subgroup.sources.extend([r1])
        db.session.add(subgroup)
        db.session.commit()
        return "Source '%s' successfully added!" % arguments['name']
    
@api.route('/input/<source_name>/new_entry', methods=['POST'])
def new_entry(source_name):
    try:
        source = db.session.query(Source).filter(
            Source.name == source_name).one()
    except NoResultFound:
        return "No source named '{}' found.".format(source_name)
    arguments = {'timestamp':'', 'body':'', 'metatags':''}
    for a in arguments.keys():
        if a in request.form:
            arguments[a] = request.form[a]
        else:
            return "Please specify '%s' argument." % a
            break
        # no duplicate checking, since it would take too much resources
    with app.app_context():
        r1 = Entry(date=datetime.datetime.fromtimestamp(
            float(arguments['timestamp'])),
                   body=arguments['body'],
                   metatags=arguments['metatags'])
        source.entries.extend([r1])
        db.session.add(source)
        db.session.commit()
        return "Entry '%s' successfully added!" % r1.id


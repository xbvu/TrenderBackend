from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
from sqlalchemy.orm.exc import NoResultFound

# Creating new Flask application.
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

"""
Database structure:

    GROUPS ->
        SUBGROUPS ->
            SOURCES ->
                ENTRY
    Example:
        Group: Twitter
        Subgroup: Hashtag
        Source: #Bitcoin
        Entry: "I bought some BTC #Bitcoin"

    Example:
        Group: Reddit
        Subgroup: Subreddit
        Source: /r/Bitcoin
        Entry: "I bought Bitcoin"

"""


# Definition of source groups table.
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    title = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=False)
    subgroups = db.relationship("Subgroup", backref="subgroups")

# Definition of subgroups table.
class Subgroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    title = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey(Group.id))
    sources = db.relationship("Source", backref="sources2")

# Definition of sources table.
class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    title = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=False)
    subgroup_id = db.Column(db.Integer, db.ForeignKey(Subgroup.id))
    entries = db.relationship("Entry", backref="entries")

# Definition of entries table.
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    added_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date = db.Column(db.DateTime, nullable=False)
    body = db.Column(db.Text, nullable=False)
    source_id = db.Column(db.Integer, db.ForeignKey(Source.id))
    metatags = db.Column(db.Text, nullable=True)
    
def build_sample_db():
    db.drop_all()
    db.create_all()
    return

@app.route('/input/new_group', methods=['POST'])
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

@app.route('/input/<group_name>/new_subgroup', methods=['POST'])
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

@app.route('/input/<subgroup_name>/new_source', methods=['POST'])
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
    
@app.route('/input/<source_name>/new_entry', methods=['POST'])
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


if __name__ == '__main__':
    # Build a sample database, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start Flask application
app.run(debug=True)

# -*- coding: utf-8 -*-

import datetime

from trender.extensions import db

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

    

#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import unittest

import sqlalchemy as sa

import db


class Repository():
    def __init__(self, host, port, dbname, user, password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password

        db.creds = {}
        db.creds['host'] = self.host
        db.creds['port'] = self.port
        db.creds['username'] = self.user
        db.creds['password'] = self.password
        db.creds['dbname'] = self.dbname
#        db.creds['use_sqlite'] = True
        db.connect()

    def create(self):
        db.conn.execute("""
create table repo (
  database_name text not null,
  schema_name text not null,
  table_name text not null,
  created_at text not null,
  data text not null
);
""")

        db.conn.execute("""
create index database_schema_table_idx
  ON repo(database_name, schema_name, table_name);
""")

        db.conn.execute("""
create index database_schema_table_created_idx
  ON repo(database_name, schema_name, table_name, created_at);
""")

        db.conn.execute("""
create table datamapping (
  lineno integer not null,
  database_name text not null,
  schema_name text not null,
  table_name text not null,
  column_name text,
  record_id text,
  source_database_name text not null,
  source_schema_name text not null,
  source_table_name text not null,
  source_column_name text,
  created_at text not null,
  data text not null
);
""")

        db.conn.execute("""
create index dm_dst_idx
  ON datamapping(database_name, schema_name, table_name);
""")

        db.conn.execute("""
create index dm_dstc_idx
  ON datamapping(database_name, schema_name, table_name, column_name);
""")

        db.conn.execute("""
create table tags (
  tag_id text not null,
  tag_label text not null
);
""")

        db.conn.execute("""
create index tags_id_idx ON tags(tag_id);
""")

        db.conn.execute("""
create index tags_label_idx ON tags(tag_label);
""")

        db.conn.execute("""
create table business_glossary (
  id text not null,
  term text not null,
  description_short text not null,
  description_long text not null,
  created_at text not null,
  owned_by text not null,
  is_latest integer not null,
  categories text,
  synonyms text,
  related_terms text,
  assigned_assets text
);
""")

        db.conn.execute("""
create table validation_rule (
  id integer primary key,
  database_name text not null,
  schema_name text not null,
  table_name text not null,
  column_name text not null,
  description text not null,
  rule text not null,
  param text,
  param2 text
);
""")

        db.conn.execute("""
create unique index validation_rule_idx on
  validation_rule(database_name,schema_name,table_name,column_name,rule,param,param2);
""")

        db.conn.execute("""
create table textelement (
  id_ text not null,
  text_ text not null
);
""")

    def destroy(self):
        self.drop_table('repo')
        self.drop_table('datamapping')
        self.drop_table('tags')
        self.drop_table('business_glossary')
        self.drop_table('validation_rule')
        self.drop_table('textelement')

    def drop_table(self, table_name):
        query = 'drop table if exists {0}'.format(table_name)
        db.conn.execute(query)


class TestRepository(unittest.TestCase):
    repo = None

    def setUp(self):
        host = os.environ.get('PGHOST', 'localhost')
        port = os.environ.get('PGPORT', 5432)
        dbname = os.environ.get('PGDATABASE', 'datacatalog')
        user = os.environ.get('PGUSER', 'postgres')
        password = os.environ.get('PGPASSWORD', 'postgres')

        self.repo = Repository(host=host,
                               port=port,
                               dbname=dbname,
                               user=user,
                               password=password)
        self.maxDiff = None

    def tearDown(self):
        self.repo.destroy()

    def test_create_001(self):
        self.repo.create()

        with self.assertRaises(sa.exc.ProgrammingError) as cm:
            self.repo.create()
        self.assertTrue(str(cm.exception).startswith('(psycopg2.ProgrammingError) relation "repo" already exists'))

    def test_destroy_001(self):
        self.repo.create()
        self.repo.destroy()

        self.repo.create()


if __name__ == '__main__':
    unittest.main()

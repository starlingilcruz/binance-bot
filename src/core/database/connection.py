#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from pymongo import MongoClient

def get_database(name = 'default'):
  return MongoClient(
        host = ['mongo-db:27017'],
        serverSelectionTimeoutMS = 3000,
        username = "root",
        password = "root",
    )[name]
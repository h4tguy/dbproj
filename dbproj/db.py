import psycopg2

import config

def connect_database():
    return psycopg2.connect('host=%s user=%s password=%s' % (config.DB_HOST, config.USER, config.PASSWORD))

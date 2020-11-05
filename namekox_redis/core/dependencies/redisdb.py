#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from redis import StrictRedis
from namekox_core.core.friendly import AsLazyProperty
from namekox_redis.constants import REDISDB_CONFIG_KEY
from namekox_core.core.service.dependency import Dependency


class RedisDB(Dependency):
    def __init__(self, dbname, **options):
        self.connection = None
        self.dbname = dbname
        self.options = options
        super(RedisDB, self).__init__(dbname, *options)

    @AsLazyProperty
    def uris(self):
        return self.container.config.get(REDISDB_CONFIG_KEY, {})

    def setup(self):
        duri = self.uris[self.dbname]
        self.connection = StrictRedis.from_url(duri, *self.options)

    def get_instance(self, context):
        return self.connection

    def stop(self):
        self.connection and self.connection.close()
        self.connection.connection_pool and self.connection.connection_pool.disconnect()
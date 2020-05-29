''' Configuration for your application '''
# Examples for 
# https://flask.palletsprojects.com/en/1.1.x/config/
# ====================================
# Examples
# ====================================
# DEBUG = False
# SECRET_KEY = key
# TESTING = False
# DATABASE_URI = 'sqlite:///:memory:'
# DB_SERVER = 'IP'
# ====================================
# Other Examples
# ====================================
# class Config(object):
#     """Base config, uses staging database server."""
#     DEBUG = False
#     TESTING = False
#     DB_SERVER = 'IP'

#     @property
#     def DATABASE_URI(self):         # Note: all caps
#         return 'mysql://user@{}/foo'.format(self.DB_SERVER)

# class ProductionConfig(Config):
#     """Uses production database server."""
#     DB_SERVER = 'IP'

# class DevelopmentConfig(Config):
#     DB_SERVER = 'localhost'
#     DEBUG = True

# class TestingConfig(Config):
#     DB_SERVER = 'localhost'
#     DEBUG = True
#     DATABASE_URI = 'sqlite:///:memory:'

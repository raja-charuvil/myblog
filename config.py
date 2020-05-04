import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'sqlite:///' + os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv('SECRET_KEY', 'I-am-not-gonna-tell-you')

    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'raja@email.com')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'test')

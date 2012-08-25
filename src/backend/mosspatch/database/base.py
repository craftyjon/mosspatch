from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MosspatchDatabase:

    def __init__(self, config):
        dbname = config.get("database", "settings-database")
        self.engine = create_engine("sqlite:///%s" % dbname)
        Base.metadata.create_all(self.engine)
        self.sessionfactory = sessionmaker(bind=self.engine)
        self.session = self.sessionfactory()

 #   def session(self):
 #       return self.sessionfactory()

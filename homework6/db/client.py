"""Module of database client"""

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from db.models import Base


class MySQLClient:
    """MySQLClient class"""

    def __init__(self, db_name, user, password):
        self.user = user
        self.port = '3306'
        self.password = password
        self.host = '127.0.0.1'
        self.db_name = db_name

        self.connection = None
        self.engine = None
        self.session = None

    def connect(self, db_created=True):
        """Connect to database session"""

        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def create_db(self):
        """Creates database"""

        self.connect(db_created=False)
        self.execute_query(f'DROP database IF EXISTS {self.db_name}')
        self.execute_query(f'CREATE database {self.db_name}')

    def create_table_total_num(self):
        if not sqlalchemy.inspect(self.engine).has_table('total_number_of_requests'):
            Base.metadata.tables['total_number_of_requests'].create(self.engine)

    def create_table_types(self):
        if not sqlalchemy.inspect(self.engine).has_table('number_of_requests_by_type'):
            Base.metadata.tables['number_of_requests_by_type'].create(self.engine)

    def create_table_top_requests(self):
        if not sqlalchemy.inspect(self.engine).has_table('top_requests'):
            Base.metadata.tables['top_requests'].create(self.engine)

    def create_table_top_4xx_requests(self):
        if not sqlalchemy.inspect(self.engine).has_table('top_4xx_requests'):
            Base.metadata.tables['top_4xx_requests'].create(self.engine)

    def create_table_top_5xx_users(self):
        if not sqlalchemy.inspect(self.engine).has_table('top_5xx_users'):
            Base.metadata.tables['top_5xx_users'].create(self.engine)

    def execute_query(self, query, fetch=False):
        """Execute provided query"""

        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

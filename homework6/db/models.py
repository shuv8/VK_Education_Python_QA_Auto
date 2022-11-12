from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR

Base = declarative_base()


class TotalNumModel(Base):

    __tablename__ = 'total_number_of_requests'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'Total number of requests={self.number_of_requests}'

    number_of_requests = Column(Integer, primary_key=True)


class TypesNumModel(Base):

    __tablename__ = 'number_of_requests_by_type'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'Number of {self.type} requests = {self.number_of_requests}'

    type = Column(VARCHAR(50), primary_key=True)
    number_of_requests = Column(Integer, nullable=False)


class TopRequestsModel(Base):

    __tablename__ = 'top_requests'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'{self.path} - {self.number_of_requests}'

    path = Column(VARCHAR(500), primary_key=True)
    number_of_requests = Column(Integer, nullable=False)


class Top4xxRequestsModel(Base):

    __tablename__ = 'top_4xx_requests'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'{self.path} - {self.response_code} - {self.size} - {self.ip}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(VARCHAR(500), nullable=True)
    response_code = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    ip = Column(VARCHAR(20), nullable=False)


class Top5xxUsersModel(Base):

    __tablename__ = 'top_5xx_users'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'{self.ip} - {self.number_of_requests}'

    ip = Column(VARCHAR(20), primary_key=True)
    number_of_requests = Column(Integer, nullable=False)

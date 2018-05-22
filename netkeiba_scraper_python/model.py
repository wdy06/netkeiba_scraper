from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, CHAR, DATE, DATETIME, ForeignKey, create_engine
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    return create_engine(get_project_settings().get('CONNECTION_STRING'))


def create_table(engine):
    Base.metadata.create_all(engine)


class Race(Base):
    __tablename__ = 'race'

    id = Column(Integer, primary_key=True)
    date = Column(DATETIME)
    race_number = Column(Integer)
    race_name = Column(String)
    special_race = Column(String)
    plain_obstacle = Column(String)
    course = Column(String)
    distance = Column(Integer)
    age_condition = Column(Integer)
    race_condition = Column(String)
    racetrack = Column(String)
    entry_restrict = Column(String)
    weight_condition = Column(String)
    grade = Column(String)
    entry_count = Column(Integer)
    weather = Column(String)
    track_condition = Column(String)
    netkeiba_url = Column(String)


class Horse(Base):
    __tablename__ = 'horse'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birthdate = Column(String)
    winnings_prize = Column(Integer)
    trainer = Column(String)
    url = Column(String)


class Jockey(Base):
    __tablename__ = 'jockey'

    id = Column(String, primary_key=True)
    name = Column(String)
    url = Column(String)


class RaceHorse(Base):
    __tablename__ = 'race_horse'

    race_id = Column(Integer, ForeignKey(Race.id), primary_key=True)
    goal_rank = Column(Integer)
    frame_number = Column(Integer)
    horse_number = Column(Integer)
    horse_id = Column(Integer, ForeignKey(Horse.id), primary_key=True)
    jockey_id = Column(Integer, ForeignKey(Jockey.id))
    time = Column(String)
    agari = Column(Integer)
    popular_rank = Column(Integer)
    horse_weight = Column(Integer)
    age = Column(Integer)


class RaceResult(Base):
    __tablename__ = 'race_result'

    race_id = Column(Integer, ForeignKey(Race.id), primary_key=True)
    odds_tansyo = Column(Integer)
    odds_hukusyo = Column(Integer)
    odds_wakuren = Column(Integer)
    odds_umaren = Column(Integer)
    odds_wide = Column(Integer)
    odds_umatan = Column(Integer)
    odds_sanrenpuku = Column(Integer)
    odds_sanrentan = Column(Integer)
    combi_tansyo = Column(Integer)
    combi_hukusyo = Column(Integer)
    combi_wakuren = Column(Integer)
    combi_umaren = Column(Integer)
    combi_wide = Column(Integer)
    combi_umatan = Column(Integer)
    combi_sanrenpuku = Column(Integer)
    combi_sanrenpuku = Column(Integer)

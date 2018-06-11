from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, REAL, ForeignKey, create_engine
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    return create_engine(get_project_settings().get('CONNECTION_STRING'))


def create_table(engine):
    Base.metadata.create_all(engine)


class Race(Base):
    __tablename__ = 'race'

    id = Column(String, primary_key=True)
    name = Column(String)
    date = Column(String)
    race_number = Column(Integer)
    race_name = Column(String)
    plain_obstacle = Column(String)
    course_field = Column(String)
    leftright = Column(String)
    distance = Column(Integer)
    age_condition = Column(Integer)
    race_grade = Column(String)
    racetrack = Column(String)
    entry_restrict = Column(String)
    weight_condition = Column(String)
    entry_count = Column(Integer)
    weather = Column(String)
    track_condition = Column(String)
    netkeiba_url = Column(String)


class Horse(Base):
    __tablename__ = 'horse'

    id = Column(String, primary_key=True)
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

    race_id = Column(String, ForeignKey(Race.id), primary_key=True)
    goal_rank = Column(Integer)
    frame_number = Column(Integer)
    horse_number = Column(Integer)
    horse_id = Column(String, ForeignKey(Horse.id), primary_key=True)
    jockey_id = Column(String, ForeignKey(Jockey.id))
    time = Column(REAL)
    agari = Column(REAL)
    tansyo_odds = Column(REAL)
    popular_rank = Column(Integer)
    horse_weight = Column(Integer)
    sex_age = Column(Integer)
    burden_weight = Column(Integer)
    netkeiba_url = Column(String)


class RaceResult(Base):
    __tablename__ = 'race_result'

    race_id = Column(String, ForeignKey(Race.id), primary_key=True)
    odds_tansyo = Column(Integer)
    odds_hukusyo_1 = Column(Integer)
    odds_hukusyo_2 = Column(Integer)
    odds_hukusyo_3 = Column(Integer)
    odds_wakuren = Column(Integer)
    odds_umaren = Column(Integer)
    odds_wide_1 = Column(Integer)
    odds_wide_2 = Column(Integer)
    odds_wide_3 = Column(Integer)
    odds_umatan = Column(Integer)
    odds_sanrenpuku = Column(Integer)
    odds_sanrentan = Column(Integer)
    combi_tansyo = Column(String)
    combi_hukusyo_1 = Column(String)
    combi_hukusyo_2 = Column(String)
    combi_hukusyo_3 = Column(String)
    combi_wakuren = Column(String)
    combi_umaren = Column(String)
    combi_wide_1 = Column(String)
    combi_wide_2 = Column(String)
    combi_wide_3 = Column(String)
    combi_umatan = Column(String)
    combi_sanrenpuku = Column(String)
    combi_sanrenpuku = Column(String)

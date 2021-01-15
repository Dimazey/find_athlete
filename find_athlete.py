import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = 'sqlite:///sochi_athletes.sqlite3'
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.INTEGER, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)

class Athelete(Base):
    __tablename__ = 'athelete'
    id = sa.Column(sa.INTEGER, primary_key=True)
    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.INTEGER)
    gold_medals = sa.Column(sa.INTEGER)
    silver_medals = sa.Column(sa.INTEGER)
    bronze_medals = sa.Column(sa.INTEGER)
    total_medals = sa.Column(sa.INTEGER)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def nearest_birthdate_athlete(user_birthdate):
    session = connect_db()
    query = session.query(Athelete)
    list_birst_dates = [Athelete.birthdate for Athelete in query.all()]
    if user_birthdate >= max(list_birst_dates):
        nearest_birthdate = max(list_birst_dates)
    elif user_birthdate <= min(list_birst_dates):
        nearest_birthdate = min(list_birst_dates)
    else:
        list_birst_dates.append(user_birthdate)
        list_birst_dates.sort()
        index_birthdate = list_birst_dates.index(user_birthdate)
        user_birthdate_num = int(user_birthdate.replace('-', ''))
        older_birthdate_num = int(list_birst_dates[index_birthdate - 1].replace('-', ''))
        yonger_birthdate_num = int(list_birst_dates[index_birthdate + 1].replace('-', ''))
        if user_birthdate_num - older_birthdate_num <= yonger_birthdate_num - user_birthdate_num:
            nearest_birthdate = list_birst_dates[index_birthdate - 1]
        else: nearest_birthdate = list_birst_dates[index_birthdate + 1]
    near_athlete_birth_name = session.query(Athelete).filter(Athelete.birthdate == nearest_birthdate).first().name    
    return (near_athlete_birth_name, nearest_birthdate)

def nearest_height_athlete(user_height):
    session = connect_db()
    query = session.query(Athelete).filter(Athelete.height != None)
    list_heights = [Athelete.height for Athelete in query.all()]
    min_height = min(list_heights)
    max_height = max(list_heights)
    if user_height <= min_height:
        near_athlete_height = min_height
    elif user_height >= max_height:
        near_athlete_height = max_height
    else:
        query = session.query(Athelete).filter(Athelete.height > user_height)
        athlete_height_tall = min([Athelete.height for Athelete in query.all()])
        query = session.query(Athelete).filter(Athelete.height <= user_height)
        athlete_height_lower = max([Athelete.height for Athelete in query.all()])
        if user_height - athlete_height_lower <= athlete_height_tall - user_height:
            near_athlete_height = athlete_height_lower
        else: near_athlete_height = athlete_height_tall
    near_athlete_height_name = session.query(Athelete).filter(Athelete.height == near_athlete_height).first().name
    return near_athlete_height_name, near_athlete_height


def main():
    print('Будем искать ближайших к пользователю участников игр по дате рождения и по росту.')
    find_email = input('Введите адрес электронной почты пользователя для поиска: ')
    session = connect_db()
    query_user = session.query(User).filter(User.email == find_email).first()
    if query_user:
        print('Ближайший по возрасту атлет: {}.  Дата рождения: {}'.format(*nearest_birthdate_athlete(query_user.birthdate)))
        print('Ближайший по росту атлет: {}. Рост: {}'.format(*nearest_height_athlete(query_user.height)))
    else: print('Пользователя с такой электронной почтой не существует')


if __name__ == '__main__':
    main()
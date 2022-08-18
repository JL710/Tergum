import functools
from pathlib import Path
from sqlite3 import DatabaseError

# import sqlalchemy
import sqlalchemy as sqla
from sqlalchemy import orm 
from sqlalchemy.exc import OperationalError



Base = orm.declarative_base()


class Profile(Base):
    __tablename__ = "profiles"

    id = sqla.Column(sqla.Integer, primary_key=True)
    name = sqla.Column(sqla.String, unique=True, nullable=False)

    cargo = orm.relationship("Cargo", back_populates="profile", cascade="all, delete, delete-orphan")

    def __repr__(self) -> str:
        return f"<Profile id={self.id} name={self.name} cargo={self.cargo}>"


class Cargo(Base):
    __tablename__ = "cargos"

    id = sqla.Column(sqla.Integer, primary_key=True)
    path = sqla.Column(sqla.String, nullable=False)

    profile_id = sqla.Column(sqla.Integer, sqla.ForeignKey("profiles.id"), nullable=False)

    profile = orm.relationship("Profile", back_populates="cargo")

    def __repr__(self) -> str:
        return f"<Cargo id={self.id} path={self.path} profile_id={self.profile_id} cargo={self.cargo}>"


class DBManager:

    __engine = sqla.create_engine(f"sqlite:///{Path(__file__).parent / 'database.db'}", echo=True)
    __session = orm.Session(bind=__engine)

    def __check_db_exist(method):
        @functools.wraps(method)
        def inner(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except OperationalError:
                Base.metadata.create_all(DBManager.__engine)
            return method(*args, **kwargs)
        return inner

    @__check_db_exist
    def new_profile(name):
        print(DBManager.__session.query(Profile).filter_by(name=name).all())
        if DBManager.__session.query(Profile).filter_by(name=name).all() != []:
            raise DatabaseError(f"Profile {name} already exists")
        print(name)
        profile = Profile(name=name)
        DBManager.__session.add(profile)
        DBManager.__session.commit()

    @__check_db_exist
    def rename_profile(old_name, new_name):
        profile = DBManager.__session.query(Profile).filter_by(name=old_name).one()
        profile.name = new_name
        DBManager.__session.commit()

    @__check_db_exist
    def delete_profile(name):
        try:
            profile = DBManager.__session.query(Profile).filter_by(name=name).one()
        except sqla.exc.NoResultFound:
            raise DatabaseError(f"Profile {name} does not exist")
        DBManager.__session.delete(profile)
        DBManager.__session.commit()

    # check if profile exists in the database
    @__check_db_exist
    def profile_exists(name) -> bool:
        if DBManager.__session.query(Profile).filter_by(name=name).one_or_none() == None:
            return False
        return True

    def recreate_db():
        Base.metadata.create_all(DBManager.__engine)


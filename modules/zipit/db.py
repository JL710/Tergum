import functools, typing
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
    target = orm.relationship("Target", back_populates="profile", cascade="all, delete, delete-orphan", uselist=False)

    def __repr__(self) -> str:
        return f"<Profile id={self.id} name={self.name} target={self.target} cargo={self.cargo}>"


class Cargo(Base):
    __tablename__ = "cargos"

    id = sqla.Column(sqla.Integer, primary_key=True)
    path = sqla.Column(sqla.String, nullable=False)

    profile_id = sqla.Column(sqla.Integer, sqla.ForeignKey("profiles.id"), nullable=False)

    profile = orm.relationship("Profile", back_populates="cargo")

    def __repr__(self) -> str:
        return f"<Cargo id={self.id} path={self.path} profile_id={self.profile_id}>"


class Target(Base):
    __tablename__ = "targets"

    id = sqla.Column(sqla.Integer, primary_key=True)
    path = sqla.Column(sqla.String, nullable=False)

    profile_id = sqla.Column(sqla.Integer, sqla.ForeignKey("profiles.id"), nullable=False, unique=True)

    profile = orm.relationship("Profile", back_populates="target")

    def __repr__(self) -> str:
        return f"<Target id={self.id} path={self.path} profile_id={self.profile_id}>"


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

    @__check_db_exist
    def get_profiles() -> typing.List[str]:
        profile_objects = DBManager.__session.query(Profile).all()
        profile_names = [profile.name for profile in profile_objects]
        return profile_names

    @__check_db_exist
    def get_cargo(profile) -> typing.List[Path]:
        profile_obj = DBManager.__session.query(Profile).filter_by(name=profile).one()
        cargo_obj = profile_obj.cargo
        path_list = []
        for c in cargo_obj:
            path_list.append(c.path)
        print(path_list)
    
    @__check_db_exist
    def add_cargo(profile: str, path: str):
        profile_obj = DBManager.__session.query(Profile).filter_by(name=profile).one()
        new_cargo = Cargo(path=path)
        profile_obj.cargo = profile_obj.cargo + [new_cargo]
        DBManager.__session.commit()

    @__check_db_exist
    def set_target(profile: str, target: str):
        """Set the target/destination for the profile"""
        profile_obj = DBManager.__session.query(Profile).filter_by(name=profile).one_or_none()
        if profile_obj.target == None:
            target_obj = Target(path=target)
        else:
            target_obj = profile_obj.target
        target_obj.path = target
        profile_obj.target = target_obj
        DBManager.__session.commit()

    @__check_db_exist
    def get_target(profile: str) -> Path:
        profile_obj = DBManager.__session.query(Profile).filter_by(name=profile).one()
        target_obj = profile_obj.target
        if target_obj == None:
            return None
        return target_obj.path

    def recreate_db():
        Base.metadata.create_all(DBManager.__engine)


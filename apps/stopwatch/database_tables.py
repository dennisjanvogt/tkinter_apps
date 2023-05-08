import os
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Stopwatches(Base):
    __tablename__ = "stopwatches"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projekte.id"))
    first_start_time = Column(DateTime, default=None, nullable=True)
    latest_start_time = Column(Float)
    state = Column(Enum("running", "paused", name="stopwatch_states"), default="paused")
    actual_time = Column(Float)
    note = Column(String, default="", nullable=True)

    project = relationship("Projekte", back_populates="stopwatches")


class Entrys(Base):
    __tablename__ = "eintraege"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projekte.id"))
    time = Column(String)
    first_start_time = Column(DateTime, nullable=True)
    note = Column(String, default="", nullable=True)

    project = relationship("Projekte")


class Projekte(Base):
    __tablename__ = "projekte"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    stopwatches = relationship("Stopwatches", back_populates="project")


db_path = os.path.join("apps/stopwatch/databases", "stopwatch.db")
engine = create_engine(f"sqlite:///{db_path}")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

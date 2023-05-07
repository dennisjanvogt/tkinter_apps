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
    start_time = Column(DateTime, default=None, nullable=True)
    state = Column(Enum("running", "paused", name="stopwatch_states"), default="paused")
    note = Column(String, default="", nullable=True)

    project = relationship("Projekte", back_populates="stopwatches")
    entries = relationship("Entrys", back_populates="stopwatch")


class Entrys(Base):
    __tablename__ = "eintraege"

    id = Column(Integer, primary_key=True)
    stopwatch_id = Column(Integer, ForeignKey("stopwatches.id"))
    project_id = Column(Integer, ForeignKey("projekte.id"))
    time = Column(Float)
    start_time = Column(DateTime, nullable=True)
    note = Column(String, default="", nullable=True)

    stopwatch = relationship("Stopwatches", back_populates="entries")
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

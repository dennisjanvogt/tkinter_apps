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


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=True)
    phone = Column(String(200), nullable=True)
    email = Column(String(200), nullable=True)
    date_created = Column(DateTime, default=func.now(), nullable=True)

    def __repr__(self):
        return self.name


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=True)
    price = Column(Float, nullable=True)
    category = Column(String(200), nullable=True)
    description = Column(String(200), nullable=True)
    date_created = Column(DateTime, default=func.now(), nullable=True)

    def __repr__(self):
        return self.name


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=True)
    customer = relationship("Customer", backref="orders")
    product_id = Column(Integer, ForeignKey("product.id"), nullable=True)
    product = relationship("Product", backref="orders")
    date_created = Column(DateTime, default=func.now(), nullable=True)
    status = Column(Enum("Pending", "Out for delivery", "Delivered"), nullable=True)
    note = Column(String(1000), nullable=True)

    def __repr__(self):
        return self.product.name


db_path = os.path.join("apps/ivy_erp/databases", "ivy.db")
engine = create_engine(f"sqlite:///{db_path}")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

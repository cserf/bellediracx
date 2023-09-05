from enum import Enum, auto

from sqlalchemy import (
    DateTime,
    Integer,
    JSON,
    String,
    Uuid,
    LargeBinary,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import declarative_base

from diracx.db.utils import Column, DateNowColumn, EnumColumn, NullColumn

USER_CODE_LENGTH = 8

Base = declarative_base()


class Production(Base):
    __tablename__ = "pm_Production"
    ProductionID = Column(Integer, autoincrement=True, primary_key=True)
    ProductionName = Column(String(255))
    ProductionGroup = Column(String(64))
    Status = Column(String(32))
    ValidationStatus = Column(String(32))
    OperationStatus = Column(String(32))
    Priority = Column(Integer, default=0)
    CreationDate = Column(DateTime, default=None)
    LastUpdate = Column(DateTime, default=None)
    OwnerDN = Column(String(255))
    OwnerGroup = Column(String(255))
    Datatype = Column(String(32))
    Release = Column(String(32))
    DBGlobalTag = Column(String(32))
    Campaign = Column(String(32))
    BeamEnergy = Column(String(32))
    MCEventType = Column(String(32))
    Description = Column(String(255))
    LongDescription = Column(LargeBinary)
    __table_args__ = (PrimaryKeyConstraint("ProductionID"),)

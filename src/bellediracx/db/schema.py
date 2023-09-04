from enum import Enum, auto

from sqlalchemy import (
    DateTime,
    Integer,
    JSON,
    String,
    Uuid,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import declarative_base

from diracx.db.utils import Column, DateNowColumn, EnumColumn, NullColumn

USER_CODE_LENGTH = 8

Base = declarative_base()

class StateStatus(Enum):
    """
    Status of the LFN or LPN
    """
    ToStage = auto()
    Staging = auto()
    Staged = auto()
    ToUnstage = auto()
    Unstaging = auto()
    Unstaged = auto()
    Error = auto()


class StagingBaseLPNsPARAMS(Base):
    __tablename__ = "StagingBaseLPNsPARAMS"
    ID = Column(Uuid(as_uuid=False), primary_key=True)
    BaseLPN = Column(String(255))
    #STATUS = Column("STATUS", Enum('ToStage','Staging','Staged','ToUnstage','Unstaging','Unstaged', 'Error'), default='ToStage')
    STATUS = EnumColumn(StateStatus, server_default=StateStatus.ToStage.name)
    ProductionID = Column(Integer)
    ProductionStatus = EnumColumn(Enum('', 'Done'), default='')
    Priority = Column(Integer, default=3) 
    InitialUpdate = Column(DateTime, default=None)
    LastUpdate = Column(DateTime, default=None)
    __table_args__ = (PrimaryKeyConstraint("ID"),)

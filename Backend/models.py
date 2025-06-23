from .database import Base
from sqlalchemy import Column, ForeignKey,Integer,String,Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class User_data(Base):
    __tablename__ = 'userdata'

    id = Column(Integer, primary_key = True, nullable = False)
    Clump_Thickness = Column(Integer, nullable = False)
    Uniformity_of_Cell_Size = Column(Integer, nullable = False)
    Uniformity_of_Cell_Shape = Column(Integer,nullable = False)
    Marginal_Adhesion = Column(Integer,nullable = False)
    Single_Epithelial_Cell_Size = Column(Integer,nullable = False)
    Bare_Nuclei = Column(Integer,nullable = False)
    Bland_Chromatin = Column(Integer,nullable = False)
    Normal_Nucleoli = Column(Integer,nullable = False)
    Mitoses = Column(Integer,nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default = text('now()'))


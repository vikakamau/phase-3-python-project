from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, session
from department import Department

class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    specialization = Column(String)
    department_id = Column(Integer, ForeignKey('department.id'))  

    appointments = relationship('Appointment', back_populates='doctor')
    department = relationship('Department', back_populates='doctors')
    patients = relationship('Patient', back_populates='doctor')

    def __init__(self, name, specialization, department_id):
        self.name = name
        self.specialization = specialization
        self.department_id = department_id
    @classmethod
    def find_by_name(cls, name):
        """
        Find a doctor by their name.
        """
        return session.query(cls).filter_by(name=name).first()

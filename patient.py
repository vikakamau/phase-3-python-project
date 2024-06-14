from database import session
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from doctor import Doctor

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    address = Column(String)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))  

    doctor = relationship('Doctor', back_populates='patients')
    appointments = relationship('Appointment', back_populates='patient')
    room = relationship('Room', uselist=False, back_populates='patient')

    def __init__(self, name, age, gender, address):
        self.name = name
        self.age = age
        self.gender = gender
        self.address = address

    @classmethod
    def find_patient(cls, name, age, gender, address):
        return session.query(cls).filter_by(name=name, age=age, gender=gender, address=address).first()
    
    @classmethod
    def get_patient(cls, name):
        return session.query(cls).filter_by(name=name).first()

    @staticmethod
    def add_doctor_to_patient(name, age, gender, address, doctor_name, session):
        """
        Add a doctor to a patient by providing patient details and doctor name.
        """
        patient = Patient.find_patient(name, age, gender, address)
        if not patient:
            patient = Patient(name=name, age=age, gender=gender, address=address)
            session.add(patient)

        doctor = session.query(Doctor).filter_by(name=doctor_name).first()
        if doctor:
            patient.doctor_id = doctor.id
            session.commit()
            print("Doctor added successfully to patient.")
        else:
            print("Doctor not found.")

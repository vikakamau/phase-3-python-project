from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, session
from patient import Patient

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    number = Column(String)
    type = Column(String)
    patient_id = Column(Integer, ForeignKey('patients.id'))

    patient = relationship('Patient', back_populates='room')

    def __init__(self, number, type, patient_id=None):
        self.number = number
        self.type = type
        self.patient_id = patient_id
    
    @classmethod
    def get_room_by_patient_id(cls, patient_id):
        return session.query(cls).filter_by(patient_id=patient_id).first()
    
    @staticmethod
    def allocate_room_to_patient(number, type, patient_name, patient_age, patient_gender, patient_address):
        patient = Patient.find_patient(patient_name, patient_age, patient_gender, patient_address)
        if not patient:
            patient = Patient(name=patient_name, age=patient_age, gender=patient_gender, address=patient_address)
            session.add(patient)
            session.commit()
            print("New patient created and added to the database.")

        # Allocate a room to the patient
        room = Room(number=number, type=type, patient_id=patient.id)
        session.add(room)
        session.commit()
        print(f"Room {number} allocated to patient {patient_name}.")

from database import session
from database import Base
from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from patient import Patient
from doctor import Doctor

class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))

    patient = relationship('Patient', back_populates='appointments')
    doctor = relationship('Doctor', back_populates='appointments')

    def __init__(self, date, patient_id, doctor_id):
        self.date = date
        self.patient_id = patient_id
        self.doctor_id = doctor_id

    @staticmethod
    def schedule_appointment(patient_name, patient_age, patient_gender, patient_address, doctor_name, appointment_date):
        """
        Schedule an appointment for a patient with a specific doctor on a given date.
        """
        patient = Patient.find_patient(patient_name, patient_age, patient_gender, patient_address)
        doctor = session.query(Doctor).filter_by(name=doctor_name).first()

        if patient and doctor:
            appointment = Appointment(date=appointment_date, patient_id=patient.id, doctor_id=doctor.id)
            session.add(appointment)
            session.commit()
            print("Appointment scheduled successfully.")
        else:
            print("Error: Either the patient or doctor could not be found.")

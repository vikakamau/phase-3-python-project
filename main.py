from database import session, engine, Base
from department import Department
from doctor import Doctor
from patient import Patient
from appoitment import Appointment
from datetime import datetime
from room import Room

def main():

    print("welcome to Aga-Khan Hospital Database")
    print("Choose desired field")
    print("1. Add Doctor")
    print("2. Add patient")
    print("3. search existing patient")
    print("4. search existing doctor")
    print("5. exit")

    choice =int(input("Enter choice: "))
    if choice == 1:
        add_doctor()
    elif choice == 2:
        add_patient()
    elif choice == 3:
        search_existing_patient()
    elif choice == 4:
        search_existing_doctor()
    elif choice == 5:
        exit()

def add_doctor():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    doctor_name = input("Enter doctor's name: ")
    doctor_specialization = input("Enter doctor's specialization: ")
    department_name = input("Enter doctor's department name: ")


    department = Department.get_or_create_department(department_name)
    new_doctor = Doctor(name=doctor_name, specialization=doctor_specialization, department_id=department.id)
    session.add(new_doctor)
    session.commit()
    print("Doctor added successfully.")

def add_patient():
    # Base.metadata.drop_all(engine, tables=[Patient.__table__, Appointment.__table__])
    Base.metadata.create_all(engine)

    patient_name = input("Enter patient's name: ")
    patient_age = int(input("Enter patient's age: "))
    patient_gender = input("Enter patient's gender: ")
    patient_address = input("Enter patient's address: ")
    doctor_name = input("Enter doctor's name: ")
    appointment_date_str = input("Enter appointment date (YYYY-MM-DD): ")
    appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%d')
    room_number = input("Enter room number: ")
    room_type = input("Enter room type: ")


    Patient.add_doctor_to_patient(patient_name, patient_age, patient_gender, patient_address, doctor_name, session)
    Appointment.schedule_appointment(patient_name, patient_age, patient_gender, patient_address, doctor_name, appointment_date)
    Room.allocate_room_to_patient(room_number, room_type, patient_name, patient_age, patient_gender, patient_address)

def search_existing_patient():
    patient_name = input("Enter patient's name: ")
    patient = Patient.get_patient(patient_name)

    if patient:
        room = Room.get_room_by_patient_id(patient.id)
        if room:
            print(f"Room Number: {room.number}, Room Type: {room.type}")
    else:
        print("Patient not found.")
def search_existing_doctor():
    doctor_name = input("Enter doctor's name: ")
    doctor = Doctor.find_by_name(doctor_name)

    if doctor:
        department = Department.get_or_create_department(doctor.id)
        if department:
            print(f"Doctor found: {doctor.name}")
            print(f"Department: {department.name}")
    else:
        print("Doctor not found.")




if __name__ == "__main__":
    main()

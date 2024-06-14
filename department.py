from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from database import session


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    doctors = relationship('Doctor', back_populates='department')

    def __init__(self, name):
        self.name = name

        session.add(self)
        session.commit()


    @staticmethod
    def get_or_create_department(department_name):
        """
        Get the department with the given name from the database.
        If it doesn't exist, create a new department with the given name.
        """
        department = session.query(Department).filter_by(name=department_name).first()

        if department:
            return department
        else:
            new_department = Department(name=department_name)
            session.add(new_department)
            session.commit()
            return new_department
    
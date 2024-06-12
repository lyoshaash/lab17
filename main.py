from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
from datetime import date

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    courses = relationship("CourseStudentAssociation", back_populates="student")

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    responsible_teacher = Column(String)
    students = relationship("CourseStudentAssociation", back_populates="course")

class CourseStudentAssociation(Base):
    __tablename__ = 'course_student_association'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    student_id = Column(Integer, ForeignKey('students.id'))
    course = relationship("Course", back_populates="students")
    student = relationship("Student", back_populates="courses")

engine = create_engine('sqlite:///courses.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

student1 = Student(name="Алексей Абдуллин", email="aleksei@example.com")
student2 = Student(name="Максим Абдуллин", email="maksim@example.com")
student3 = Student(name="Николай Абдуллин", email="nikolai@example.com")
student4 = Student(name="Азат Абдуллин", email="azat@example.com")

course1 = Course(name="Математика", responsible_teacher="Тимур Губайдуллин")
course2 = Course(name="Физика", responsible_teacher="Арина Кадырова")
course3 = Course(name="История", responsible_teacher="Василий Платонов")
course4 = Course(name="Программирование", responsible_teacher="Игорь Бычин")

association1 = CourseStudentAssociation(course=course1, student=student1)
association2 = CourseStudentAssociation(course=course2, student=student2)
association3 = CourseStudentAssociation(course=course3, student=student3)
association4 = CourseStudentAssociation(course=course4, student=student4)

session.add(student1)
session.add(student2)
session.add(student3)
session.add(student4)
session.add(course1)
session.add(course2)
session.add(course3)
session.add(course4)
session.add(association1)
session.add(association2)
session.add(association3)
session.add(association4)
session.commit()

def get_student_courses(student_name):
    return session.query(Course).join(CourseStudentAssociation).join(Student).filter(Student.name == student_name).all()

def get_courses_by_teacher(teacher_name):
    return session.query(Course).filter(Course.responsible_teacher == teacher_name).all()

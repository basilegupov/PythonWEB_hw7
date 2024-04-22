from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from conf.models import Base, Professor, Group, Student, Subject, Grade
from conf.db import URI
import random

fake = Faker('uk_UA')

# Подключение к базе данных
engine = create_engine(URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Добавление групп
for _ in range(3):
    group = Group(name=fake.word())
    session.add(group)

# Добавление преподавателей
for _ in range(3):
    professor = Professor(fullname=fake.name())
    session.add(professor)

# Добавление предметов с указанием преподавателя
professors = session.query(Professor).all()
for _ in range(2):
    for professor in professors:
        subject = Subject(name=fake.word(), professor=professor)
        session.add(subject)

# Добавление студентов и оценок
groups = session.query(Group).all()
subjects = session.query(Subject).all()
for _ in range(10):
    for group in groups:
        student = Student(fullname=fake.name(), group=group)
        session.add(student)
        session.flush()  # Получаем ID добавленного студента
        for subject in subjects:
            for _ in range(3):
                grade = Grade(student=student, discipline=subject,
                              grade=random.randint(0, 100), grade_date=fake.date_this_decade())
                session.add(grade)

# Сохранение изменений
session.commit()

# Закрытие соединения
session.close()

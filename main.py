from sqlalchemy import func, desc, and_

from conf.models import Grade, Group, Professor, Student, Subject
from conf.db import session


def select_1():
    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .join(Grade) \
        .group_by(Student.id) \
        .order_by(desc('avg_grade')) \
        .limit(5).all()
    return result

def select_2(subject_name):
    # Знайти студента із найвищим середнім балом з певного предмета.
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .join(Grade) \
        .join(Subject) \
        .filter(Subject.name == subject_name) \
        .group_by(Student.id) \
        .order_by(desc('avg_grade')) \
        .first()
    return result

def select_3(subject_name):
    # Знайти середній бал у групах з певного предмета.
    result = session.query(Group.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .join(Student, Group.id == Student.group_id) \
        .join(Grade, Student.id == Grade.student_id) \
        .join(Subject, Grade.subjects_id == Subject.id) \
        .filter(Subject.name == subject_name) \
        .group_by(Group.name) \
        .all()
    return result

def select_4():    
    #Знайти середній бал на потоці (по всій таблиці оцінок).
    result = session.query(func.round(func.avg(Grade.grade), 2)\
    .label('avg_grade'))\
    .select_from(Grade)\
    .all()
    return result

def select_5(professor_id):
    # Знайти які курси читає певний викладач.
    result = session.query(Subject.name).join(Professor).filter(Professor.id == professor_id).all()
    return [subject.name for subject in result]

def select_6(group_id):
    # Знайти список студентів у певній групі.
    result = session.query(Student.fullname).filter(Student.group_id == group_id).all()
    return [student.fullname for student in result]

def select_7(group_id, subject_name):
    # Знайти оцінки студентів у окремій групі з певного предмета.
    result = session.query(Student.fullname, Grade.grade) \
        .join(Grade) \
        .join(Subject) \
        .filter(Student.group_id == group_id, Subject.name == subject_name) \
        .all()
    return result

def select_8(professor_name):
    # Знайти середній бал, який ставить певний викладач зі своїх предметів.
    result = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .join(Subject) \
        .join(Professor) \
        .filter(Professor.fullname == professor_name) \
        .first()
    return result[0] if result is not None else None

def select_9(student_id):
    # Знайти список курсів, які відвідує певний студент.
    result = session.query(Subject.name).join(Grade).join(Student).filter(Student.id == student_id).group_by(Subject.name).all()
    return [subject.name for subject in result]

def select_10(student_id, professor_id):
    # Список курсів, які певному студенту читає певний викладач.
    result = session.query(Subject.name).join(Professor).join(Grade).join(Student) \
        .filter(Student.id == student_id, Professor.id == professor_id).group_by(Subject.name).all()
    return [subject.name for subject in result]

def select_11(student_id, professor_id):
    # Середній бал, який певний викладач ставить певному студентові.
    result = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .join(Student) \
        .join(Subject) \
        .join(Professor) \
        .filter(Student.id == student_id, Professor.id == professor_id) \
        .first()
    return result[0] if result else None

def select_12(group_id, subject_name):
    # Оцінки студентів у певній групі з певного предмета на останньому занятті.
    subquery = session.query(Student.id, func.max(Grade.grade_date).label('max_grade_date')) \
        .join(Grade) \
        .join(Subject) \
        .filter(Student.group_id == group_id, Subject.name == subject_name) \
        .group_by(Student.id).subquery()

    result = session.query(Student.fullname, Grade.grade) \
        .join(Grade) \
        .join(Subject) \
        .join(subquery, and_(Student.id == subquery.c.id, Grade.grade_date == subquery.c.max_grade_date)) \
        .filter(Student.group_id == group_id, Subject.name == subject_name) \
        .all()
    return result

def format_result(result):
    formatted_result = "[\n"
    for item in result:
        formatted_result += f"  {item},\n"
    formatted_result += "]"
    return formatted_result


if __name__ == '__main__':
    try:
        print("Query 1:")
        print(format_result(select_1()))
        print("Query 2:")
        print(format_result(select_2("демократія")))
        print("Query 3:")
        print(format_result(select_3("демократія")))
        print("Query 4:")
        print(f"Середній бал на потоці: {select_4()}")
        print("Query 5:")
        print(format_result(select_5(1)))
        print("Query 6:")
        print(format_result(select_6(3)))
        print("Query 7:")
        print(format_result(select_7(2, "демократія")))
        print("Query 8:")
        print(f"Середній бал, який ставить певний викладач зі своїх предметів: {select_8("Арсен Вернигора")}")
        print("Query 9:")
        print(format_result(select_9(5)))
        print("Query 10:")
        print(format_result(select_10(8, 1)))
        print("Query 11:")
        print(f"Середній бал, який певний викладач ставить певному студентові: {select_11(8, 1)}")
        print("Query 12:")
        print(format_result(select_12(2, "демократія")))
    except Exception as e:
        print("Error:", e)
    finally:
        session.close()
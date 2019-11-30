from . import db

(Column, ForeignKey, Model, Table) = (db.Column, db.ForeignKey, db.Model, db.Table)
(relationship, backref) = (db.relationship, db.backref)
(Integer, String, Decimal) = (db.Integer, db.String, db.Decimal)

# from flask_sqlalchemy import BaseQuery, SQLAlchemy  # if we create custom query
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy import or_
# from datetime import datetime as dt
# from dateutil import parser
# from pprint import pprint  # only for debugging

# ===================================================================================================================
# student to book         => One-to-Many  # ForeignKey on One, relationship on Second.
# student to year         => Many-to-One  # ForeignKey & relationship on One.
# student to locker       => One-to-One   # ForeignKey & relationship on One.
# student to classroom    => Many-to-Many # Relationship on One, 2 ForeignKeys on needed association_table.
# student to subject      => Many-to-Many # Relationship on Both, 2 ForeignKeys & 2 Relationships on Associated Object (class).
# student-student popular => Many-to-Many # 1 relationship on Student, 2 ForeignKeys on assoc_table
# student-student Clubs   => Many-to-Many # 2 relationships on Club, 2 assoc_table, each w/ 2 ForeignKeys (Club, leader|member)
# ===================================================================================================================

hierarchy = Table(
    'hierarchy',  # Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('superior_id', Integer, ForeignKey('Student.id')),
    Column('report_id',  Integer, ForeignKey('Student.id'))
)

popular = Table(
    'popular',  # Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('high_regard_id', Integer, ForeignKey('Student.id')),
    Column('fan_id',  Integer, ForeignKey('Student.id'))
)


class Student(Model):
    """ Students have many types of data associations. """
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    books = relationship('Book', backref='student')
    year_id = Column(Integer, ForeignKey('years.id'))
    year = relationship('Year', backref='students')
    locker_id = Column(Integer, ForeignKey('lockers.id'))
    locker = relationship('Locker', backref=backref('student', uselist=False))
    rooms = relationship('Classroom', secondary='association_table', backref='students')
    subjects = relationship('Subject', secondary='grades')
    high_regards = relationship('Student',
                                secondary=popular,
                                primaryjoin=id == popular.c.fan_id,
                                secondaryjoin=id == popular.c.high_regard_id,
                                backref=backref('fans')
                                )
    # # reports = backref from Student.superiors
    # # leading_clubs = backref from Club.leaders
    # # joined_clubs = backref from Club.members
    # # grades = backref from Grade.student


class Book(Model):
    """ Students receive multiple textbooks that they must return. One-to-Many """
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    barcode = Column(String(255))
    condition = Column(String(255))
    student_id = Column(Integer, ForeignKey('students.id'))
    # # student = backref from Student.books


class Year(Model):
    """ Various Students have a projected year of graduation. Many-to-One """
    __tablename__ = 'years'
    id = Column(Integer, primary_key=True)
    graduation_year = Column(Integer)
    # # students = backref from Student.year


class Locker(Model):
    """ Each Student gets only one Locker. One-to-One """
    __tablename__ = 'lockers'
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    # # student = backref from Student.locker


association_table = Table(
    'student_classroom',  # Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('student_id', Integer, ForeignKey('student.id')),
    Column('classroom_id', Integer, ForeignKey('classroom.id'))
)


class Classroom(Model):
    """ Various Students are in various Classrooms in a day. Many-to-Many (simple) """
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    building = Column(String(255))
    room_num = Column(Integer)
    # # students = backref from Student.rooms


class Subject(Model):
    """ Multiple Students in multiple Subjects, with a Grade for each. Many-to-Many through Associated Object """
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    students = relationship('Student', secondary='grades')
    # # grades = backref from Grade.subject


class Grade(Model):
    """ Each Student gets a Grade for each Subject they have. Associated Object of Many-to-Many """
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    gradepoint = Column(Decimal)
    student = relationship('Student', backref=backref('grades', cascade='all, delete-orphan'))
    subject = relationship('Subject', backref=backref('grades', cascade='all, delete-orphan'))


club_leader = Table(
    'club_leader',  # Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('leader_id',  Integer, ForeignKey('students.id', ondelete="CASCADE")),
    Column('club_id',    Integer, ForeignKey('clubs.id', ondelete="CASCADE"))
)
club_member = Table(
    'club_member',  # Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('member_id',  Integer, ForeignKey('students.id', ondelete="CASCADE")),
    Column('club_id',    Integer, ForeignKey('clubs.id', ondelete="CASCADE"))
)


class Club(Model):
    """ A Student can be a member and/or a leader of many clubs, clubs have many members and leaders """
    __tablename__ = 'clubs'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    leaders = relationship('Student', secondary=club_leader, backref=backref('leading_clubs', lazy='dynamic'))
    members = relationship('Student', secondary=club_member, backref=backref('joined_clubs', lazy='dynamic'))


##################################################################################
# End of Models. Some setup functions follow below.
##################################################################################


def _create_database():
    """ This may need to be updated for it to work. """
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy

    db = SQLAlchemy()
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    app.config.setdefault('SQLALCHEMY_ECHO', True)
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        print("All tables dropped!")
        db.create_all()
        print("All tables created")


if __name__ == '__main__':
    _create_database()

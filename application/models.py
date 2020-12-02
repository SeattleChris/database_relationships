from datetime import datetime as dt
from . import db
# from flask_sqlalchemy import BaseQuery  # if we create custom query
# SQLAlchemy overloads &, |, and ~, so use them inside a filter. Paranthesis are needed around each equality check
# from sqlalchemy import or_  # this can be used with a generator to handle indeterminate number of 'OR' conditions

(Column, ForeignKey, Model, Table) = (db.Column, db.ForeignKey, db.Model, db.Table)
(relationship, backref) = (db.relationship, db.backref)
(Integer, String, Numeric) = (db.Integer, db.String, db.Numeric)

"""
===================================================================================================================
student to book         => One-to-Many  # Relationship on One, ForeignKey on Second.
student to year         => Many-to-One  # ForeignKey & relationship on One.
student to locker       => One-to-One   # ForeignKey & relationship on One.
student to classroom    => Many-to-Many # Relationship on One, 2 ForeignKeys on needed association_table.
student to subject      => Many-to-Many # Relationship on Both, 2 ForeignKeys & 2 Relationships on Associated Object (class).
student-student popular => Many-to-Many # 1 relationship on Student, 2 ForeignKeys on assoc_table
student-student Clubs   => Many-to-Many # 2 relationships on Club, 2 assoc_table, each w/ 2 ForeignKeys (Club, leader|member)
===================================================================================================================
"""

popular = Table(
    'popular',
    Column('id', Integer, primary_key=True),
    Column('high_regard_id', Integer, ForeignKey('students.id')),
    Column('fan_id',  Integer, ForeignKey('students.id'))
)

association_table = Table(
    'student_classroom',
    Column('id', Integer, primary_key=True),
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('classroom_id', Integer, ForeignKey('classrooms.id'))
)


class Student(Model):
    """ Students have many types of data associations. """
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    year_id = Column(Integer, ForeignKey('years.id'))
    locker_id = Column(Integer, ForeignKey('lockers.id'))
    modified = db.Column(db.DateTime, index=False, unique=False, nullable=False, default=dt.utcnow, onupdate=dt.utcnow)
    created = db.Column(db.DateTime,  index=False, unique=False, nullable=False, default=dt.utcnow)
    year = relationship('Year', backref='students')
    books = relationship('Book', backref='student')
    locker = relationship('Locker', backref=backref('student', uselist=False))
    rooms = relationship('Classroom', secondary=association_table, backref='students')
    subjects = relationship('Subject', secondary='grades')
    fans = relationship('Student',
                        secondary=popular,
                        primaryjoin=id == popular.c.high_regard_id,
                        secondaryjoin=id == popular.c.fan_id,
                        backref=backref('high_regards')
                        )
    # # high_regards = backref from Student.fans
    # # leading_clubs = backref from Club.leaders
    # # joined_clubs = backref from Club.members
    # # grades = backref from Grade.student

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Book(Model):
    """ Students receive multiple textbooks that they must return. One-to-Many """
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    barcode = Column(String(255))
    condition = Column(String(255))
    student_id = Column(Integer, ForeignKey('students.id'))
    # # student = backref from Student.books

    def __str__(self):
        return f"Book: {self.barcode} Held by: {self.student}"

    def __repr__(self):
        return f"Book: {self.barcode} Held by: {self.student}"


class Year(Model):
    """ Various Students have a projected year of graduation. Many-to-One """
    __tablename__ = 'years'
    id = Column(Integer, primary_key=True)
    graduation_year = Column(Integer)
    # # students = backref from Student.year

    def __str__(self):
        return str(self.graduation_year)

    def __repr__(self):
        return str(self.graduation_year)


class Locker(Model):
    """ Each Student gets only one Locker. One-to-One """
    __tablename__ = 'lockers'
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    # # student = backref from Student.locker

    def __str__(self):
        return str(self.number)

    def __repr__(self):
        return f"Locker: {self.number} Held by: {self.student}"


class Classroom(Model):
    """ Various Students are in various Classrooms in a day. Many-to-Many (simple) """
    __tablename__ = 'classrooms'
    id = Column(Integer, primary_key=True)
    building = Column(String(255))
    room_num = Column(Integer)
    # # students = backref from Student.rooms

    def __str__(self):
        return f"Class: {self.building} {self.room_num}"

    def __repr__(self):
        return f"Class: {self.building} {self.room_num}"


class Subject(Model):
    """ Multiple Students in multiple Subjects, with a Grade for each. Many-to-Many through Associated Object """
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    students = relationship('Student', secondary='grades')
    # # grades = backref from Grade.subject

    def __str__(self):
        return f"Subject: {self.name} with {len(self.students)} students"

    def __repr__(self):
        return f"Subject: {self.name} with {len(self.students)} students"


class Grade(Model):
    """ Associated Object of Many-to-Many (with extra fields).
        Essentially creating One-to-Many for Student-to-Grade and Subject-to-Grade.
        Each Student gets a Grade for the various Subjects they have (One-to-Many).
        Each Subject has a Grade for the various Students (One-to-Many).
        For any given Subject and Student combination, there is only one grade.
    """
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    gradepoint = Column(Numeric)
    student = relationship('Student', backref=backref('grades', cascade='all, delete-orphan'))
    subject = relationship('Subject', backref=backref('grades', cascade='all, delete-orphan'))
    # create a composite unique requirement of student_id & subject_id?

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.gradepoint}"

    def __repr__(self):
        return f"{self.student} - {self.subject}: {self.gradepoint}"


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
    """ A Student can be a member and/or a leader of many clubs.
        Clubs have many members and many leaders.
        Many-to-Many (self-referencing) through associated object with extra fields.
    """
    __tablename__ = 'clubs'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    leaders = relationship('Student', secondary=club_leader, backref=backref('leading_clubs', lazy='dynamic'))
    members = relationship('Student', secondary=club_member, backref=backref('joined_clubs', lazy='dynamic'))

    def __str__(self):
        count = len(self.leaders) + len(self.members)
        return f"Club: {self.name} with {count} members"

##################################################################################
# End of Models. Some setup functions follow below.
##################################################################################


# def _create_database():
#     """ This may need to be updated for it to work. """
#     from flask import Flask
#     from flask_sqlalchemy import SQLAlchemy
#     from ..config import Config

#     db = SQLAlchemy()
#     app = Flask(__name__)
#     app.config.from_object(Config)
#     app.config.setdefault('SQLALCHEMY_ECHO', True)
#     db.init_app(app)
#     with app.app_context():
#         db.drop_all()
#         print("All tables dropped!")
#         db.create_all()
#         print("All tables created")
#     return db


# if __name__ == '__main__':
#     db = _create_database()

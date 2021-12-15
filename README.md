# database_relationships

Insights on the different kinds of relationships we might use in SQL. One-to-Many, Many-to-One, One-to-One, Many-to-Many, Many-to-Many with Extra Fields on the relationship Model, etc. This demo is in Python, using Flask and Flask-SQLAlchemy. Similar concepts and structures would work for other tools and other languages.

To show the various options, we are using a school example, specifically where students have multiple subjects and visit multiple classrooms throughout the day, have an on-campus locker to store their school supplies, and other aspects you might find in a school setting.

# Models

We construct models of our data, with a model class for each type of 'thing' that has a collection of properties (and methods). Each Model will have a table in the database. There may be additional relationship tables if needed. If we have base classes, they typically do not have their own table in the database (but could in some complicated atypical setup).

We want to seperate each logical grouping of attributes into their own model without needing to store the same data in multiple places / models.
## Student

- name
- year of graduation.

For

Club (each on focusing on some kind of shared extra-curricular interest).

## Relationships

===============================================================================================================
| From 1st to 2nd    | Relationship| Where the relationship is in the code.
+--------------------+-------------+------------------------------------------------------------------------
| student - book     |One-to-Many | Relationship on One, ForeignKey on Second.
| student - year     |Many-to-One | ForeignKey & relationship on One.
| student - locker   |One-to-One  | ForeignKey & relationship on One.
| student - classroom|Many-to-Many|Relationship on One, 2 ForeignKeys on needed association_table.
| student - subject  |Many-to-Many|Relationship on Both, 2 ForeignKeys & 2 Relationships on Assoc. Object(class)
| popular (stu-stu)  |Many-to-Many|1 Student relationship, 2 ForeignKeys on assoc_table.
| Clubs (stu-stu)    |Many-to-Many|2 Club relationships, 2 assoc_table each w/ 2 ForeignKeys (leader vs member)

===============================================================================================================

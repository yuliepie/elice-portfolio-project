from project import db, bcrypt


class User(db.Model):
    """
    Represents a user of the application.

    Attributes:
        * email (string)
        * hashed password (string)
        * name (string)
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    email = db.Column(
        db.String(100), nullable=False, unique=True
    )  # user id must be unique
    password_hashed = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=True)

    educations = db.relationship("Education", backref="user", lazy=True)
    awards = db.relationship("Award", backref="user", lazy=True)
    projects = db.relationship("Project", backref="user", lazy=True)
    certifications = db.relationship("Certification", backref="user", lazy=True)

    def __init__(self, email: str, password_original: str, name: str):
        self.email = email
        self.password_hashed = bcrypt.generate_password_hash(password_original)
        self.name = name

    def is_password_correct(self, password_original: str):
        return bcrypt.check_password_hash(self.password_hashed, password_original)

    def _repr(self):
        return f"<User: {self.name} {self.email}"


class Education(db.Model):
    """
    Represents an education detail of a user.

    Attributes:
        * name (string) : 학교 이름.
        * major (string) : 전공.
        * status (integer) : 졸업상태. Foreign Key --> Education_Status
        * user (integer) : 유저. Foreign Key --> User
    """

    __tablename__ = "educations"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    school_name = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(100), nullable=False)
    status_id = db.Column(
        db.Integer, db.ForeignKey("education_status.id"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, school_name: str, major: str, status_id: int, user_id: int):
        self.school_name = school_name
        self.major = self.major
        self.status_id = status_id
        self.user_id = user_id


class EducationStatus(db.Model):
    """졸업 상태"""

    __tablename__ = "education_status"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    status_name = db.Column(db.String(30), nullable=False)
    educations = db.relationship("Education", backref="edustatus", lazy=True)

    def __init__(self, status_name: str):
        self.status_name = status_name


class Award(db.Model):
    """수상내역"""

    __tablename__ = "awards"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, name: str, description: str, user_id: int):
        self.name = name
        self.description = description
        self.user_id = user_id


#############################
# TODO: REVIEW DATE FORMAT!!!
##############################
class Project(db.Model):
    """프로젝트"""

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description: db.Column(db.String(500), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, name: str, description: str, start_date: str, end_date: str):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date


#############################
# TODO: REVIEW DATE FORMAT!!!
##############################
class Certification(db.Model):
    """자격증"""

    __tablename__ = "certifications"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    provider = db.Column(db.String(50), nullable=False)
    acquired_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, name: str, provider: str, date: str, user_id: int):
        self.name = name
        self.provider = provider
        self.acquired_date = date
        self.user_id = user_id

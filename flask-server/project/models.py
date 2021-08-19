from project import db, bcrypt
from datetime import date


class User(db.Model):
    """
    Represents a user of the application.

    Attributes:
        * email (string) : 이메일 주소
        * password_hashed (string) : 해쉬된 비밀번호
        * name (string) : 이름
        * description (string) : 한줄소개
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

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Education(db.Model):
    """
    Represents an education record of a user.

    Attributes:
        * school_name (string) : 학교 이름.
        * major (string) : 전공.
        * status_id (integer) : 졸업상태. Foreign Key --> Education_Status
        * user_id (integer) : 유저. Foreign Key --> User
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
        self.major = major
        self.status_id = status_id
        self.user_id = user_id


class EducationStatus(db.Model):
    """
    Represents the Graduation status for an education record.

    Attributes:
        * status_name (string) : 상태 이름
    """

    __tablename__ = "education_status"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    status_name = db.Column(db.String(30), nullable=False)
    educations = db.relationship("Education", backref="edustatus", lazy=True)

    def __init__(self, status_name: str):
        self.status_name = status_name


class Award(db.Model):
    """
    Represents an award record for a user.

    Attributes:
        * name (string) : 수상 내역.
        * description (string) : 상세 내역.
        * user_id (integer) : 유저. Foreign Key --> User
    """

    __tablename__ = "awards"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, name: str, description: str, user_id: int):
        self.name = name
        self.description = description
        self.user_id = user_id


class Project(db.Model):
    """
    Represents a project record for a user.

    Attributes:
        * name (string) : 프로젝트 이름.
        * description (string) : 프로젝트 설명.
        * start_date (datetime) : 시작 날짜.
        * end_date (datetime) : 종료 날짜.
        * user_id (integer) : 유저. Foreign Key --> User
    """

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description: db.Column(db.String(500), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(
        self,
        name: str,
        description: str,
        start_date: date,
        end_date: date,
        user_id: int,
    ):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.user_id = user_id


class Certification(db.Model):
    """
    Represents a certification record for a user.

    Attributes:
        * name (string) : 자격증 이름.
        * provider (string) : 자격증 발급자.
        * acquired_date (datetime) : 취득 날짜.
        * user_id (integer) : 유저. Foreign Key --> User
    """

    __tablename__ = "certifications"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    provider = db.Column(db.String(50), nullable=False)
    acquired_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, name: str, provider: str, date: date, user_id: int):
        self.name = name
        self.provider = provider
        self.acquired_date = date
        self.user_id = user_id

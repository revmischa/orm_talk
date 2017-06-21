"""ORM demonstration."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, Text, CheckConstraint, DateTime, func
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy import and_, or_

DB_DSN = 'postgresql:///orm_demo'

user1 = None
user2 = None
userpost1 = None

# our database connection and engine
engine = create_engine(DB_DSN, echo=True)

SessionFactory = sessionmaker()
# bind session factory to our postgresql connection
SessionFactory.configure(bind=engine)
# begin a session
session = SessionFactory()

# declarative schema
DemoBase = declarative_base()


class User(DemoBase):
    """Represents an account."""

    __tablename__ = 'person'  # class is User, table is named person

    id = Column(Integer, primary_key=True)

    # user's name
    name = Column(Text)

    # password
    password = Column(Text)

    # email address, TEXT NOT NULL UNIQUE
    email = Column(
        Text,
        CheckConstraint("email != ''", "empty_user_email"),
        nullable=False,
        unique=True,
    )

    # our posts
    posts = relationship('UserPost', back_populates="user")


class UserPost(DemoBase):
    """A blog posting by a user."""

    __tablename__ = 'user_post'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    body = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('person.id'), nullable=False)
    user = relationship('User', back_populates="posts")

    def __repr__(self):
        """Print pretty."""
        return f"<Blog post for user {self.user.email}, body={self.body}>"


def create_db():
    """Create database from declarative schema."""
    print("creating")
    DemoBase.metadata.drop_all(engine)
    DemoBase.metadata.create_all(engine)
    global session
    create_test_data(session)


def create_test_data(session):
    global user1, userpost1, user2
    # construct user1
    user1 = User(
        name="Demo User 1",
        email="demouser1@test.com",
    )
    # add to session
    session.add(user1)
    # commit changes
    session.commit()

    # construct user post
    userpost1 = UserPost(
        user=user1,
        body="User1 Post 1",
    )
    session.add(userpost1)
    session.commit()

    # add some more test rows
    for i in range(2, 9):
        useri = User(name=f"Demo User {i}", email=f"demouser{i}@test.com")
        session.add(useri)
        for j in range(5):
            post = UserPost(user=useri, body=f"user{i} post {j}")
            session.add(post)
    session.commit()


# entrypoint
def main():
    create_db()

if __name__ == '__main__':
    main()

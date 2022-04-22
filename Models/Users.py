import sqlalchemy as sa
import logging as log
from .DB_metadata import Base, metadata, session


third_digit = ['0', '1', '2', '3', '4', '5']


class UserAlreadyExists(Exception):
    pass


class UserWithIllegalAttributes(Exception):
    pass


class UserDoesNotExist(Exception):
    pass


class User(Base):

    __table__ = sa.Table("User", metadata)

    def __init__(self, phone: str, name: str, email: str):
        # google should check if the email is legal
        if len(phone) != 10 or not phone.isdigit() or len(name) > 50 or phone[0] != '0' or phone[1] != '5' or phone[2] not in third_digit or len(name) > 50:
            message = "Illegal user attributes"
            log.warning(message)
            raise UserWithIllegalAttributes(message)
        self.PhoneNum = phone
        self.Name = name
        self.Email = email

    @staticmethod
    def add_user(phone, name, email):
        try:
            session.add(User(phone, name, email))
            session.commit()
        except Exception as e:
            log.warning(e)
            raise UserAlreadyExists(e)

    def authenticate(self):
        pass

    def logout(self):
        pass


def get_user_by_phone(phone):
    cur = session.query(User).filter(User.PhoneNum == phone).first()
    if not cur:
        message = "User with given phone does not exist"
        log.warning(message)
        raise UserDoesNotExist(message)


def get_user_by_email(email):
    cur =  session.query(User).filter(User.Email == email).first()
    if not cur:
        message = "User with given email does not exist"
        log.warning(message)
        raise UserDoesNotExist(message)




#print(session.query(User).filter(User.PhoneNum == "0526866526").first().Name)






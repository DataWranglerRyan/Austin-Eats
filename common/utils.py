from passlib.hash import pbkdf2_sha512


class Utils(object):
    @staticmethod
    def encrypt_password(password: str) -> str:
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_encrypted_password(password: str, encrypted_password: str) -> bool:
        return pbkdf2_sha512.verify(password, encrypted_password)

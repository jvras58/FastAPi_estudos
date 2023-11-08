from app.security.auth import get_password_hash, verify_password


def test_passcrypt():
    clr_password = 'senhaadm'
    hashed_password = get_password_hash(clr_password)
    pass_test = verify_password(clr_password, hashed_password)
    assert pass_test

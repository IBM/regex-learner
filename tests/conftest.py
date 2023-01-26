import pytest


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    return ['it_IT', 'en_US']

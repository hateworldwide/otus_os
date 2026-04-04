import pymysql
import pytest


def pytest_addoption(parser):
    parser.addoption("--host", default="localhost")
    parser.addoption("--port", default=3306, type=int)
    parser.addoption("--database", default="bitnami_opencart")
    parser.addoption("--user", default="bn_opencart")
    parser.addoption("--password", default="")


@pytest.fixture(scope="session")
def connection(request):
    conn = pymysql.connect(
        host=request.config.getoption("--host"),
        port=request.config.getoption("--port"),
        user=request.config.getoption("--user"),
        password=request.config.getoption("--password"),
        database=request.config.getoption("--database"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
    yield conn
    conn.close()
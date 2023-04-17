from in_py import sql_func
import pandas as pd


def test_wall():
    sql_func.sql_start()
    df = pd.read_sql_query("SELECT * from priznavashki", sql_func.base)
    assert len(df) == 40090


def test_comments():
    sql_func.sql_start()
    df = pd.read_sql_query("SELECT * from all_comments", sql_func.base)
    assert len(df) == 11


def test_likes_comments():
    sql_func.sql_start()
    df = pd.read_sql_query("SELECT * from likes_comments", sql_func.base)
    assert len(df) == 27505


def test_users_main():
    sql_func.sql_start()
    df = pd.read_sql_query("SELECT * from users_main", sql_func.base)
    assert len(df) == 461


def test_id_comments():
    sql_func.sql_start()
    df = pd.read_sql_query("SELECT * from all_comments WHERE user_id == 2340546", sql_func.base)
    assert len(df) == 3


def test_id_likes():
    sql_func.sql_start()
    df = pd.read_sql_query("SELECT * from likes_comments WHERE user_id == 560156454", sql_func.base)
    assert len(df) == 1


def test_id_priznavashki_anon():
    sql_func.sql_start()
    df = pd.read_sql_query("SELECT * from priznavashki WHERE user_id == -59518047", sql_func.base)
    assert len(df) == 35585


def test_id_users_main():
    sql_func.sql_start()
    df = pd.read_sql_query("SELECT * from users_main WHERE user_id == -50260527", sql_func.base)
    assert len(df) == 86

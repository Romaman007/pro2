import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect(r'..\post.db')
    cur = base.cursor()
    if base:
        print('DBase connected!')
    base.execute(
        'CREATE TABLE IF NOT EXISTS users_main(post_id PRIMARY KEY,user_id INT, date_of_post VARCHAR, likes INT, comments INT, reposts INT, text VARCHAR )')
    base.execute('CREATE TABLE IF NOT EXISTS likes_comments(user_id PRIMARY KEY, likes INT, comments INT )')
    base.execute(
        'CREATE TABLE IF NOT EXISTS all_comments(comment_id PRIMARY KEY,user_id INT,post_id INT, likes INT,text VARCHAR, date_of_comment VARCHAR,likes_id INT )')
    base.commit()


def create_table():
    base.execute(
        'CREATE TABLE IF NOT EXISTS priznavashki(post_id PRIMARY KEY,user_id INT, date_of_post VARCHAR, likes INT, comments INT,reposts INT,text VARCHAR )')


def add_post(id, owner_id, date, likes, comments, reposts, text):
    cur.execute('INSERT INTO priznavashki VALUES (?,?,?,?,?,?,?)', (id, owner_id, date, likes, comments, reposts, text))
    base.commit()


def add_post_search(id, owner_id, date, likes, comments, reposts, text):
    cur.execute('INSERT INTO users_main VALUES (?,?,?,?,?,?,?)', (id, owner_id, date, likes, comments, reposts, text))
    base.commit()


def add_user_likes(id, likes, comments):
    cur.execute('INSERT INTO likes_comments VALUES (?,?,?)', (id, likes, comments))
    base.commit()


def check(data):
    dat = cur.execute('SELECT likes,comments FROM likes_comments WHERE user_id== ?', (data,)).fetchone()
    return dat


def add_comment(id, user_id, post_id, likes, text, data, lk_array):
    cur.execute('INSERT INTO all_comments VALUES (?,?,?,?,?,?,?)', (id, user_id, post_id, likes, text, data, lk_array))
    base.commit()

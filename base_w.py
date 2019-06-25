import sqlite3

def init_admin(id, username, nickname):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    if username == None:
        username = 'None'
    cursor.execute('INSERT INTO admins (id, username, nick_name) VALUES (?, ?, ?)',
                   (id, '@'+username, nickname))
    conn.commit()
    cursor.close()
    conn.close()

def all_admins():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admins')
    idin = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    a = []

    for i in idin:
        l = str(i[1]) + '  ' +str(i[2])
        a.append(l)
    return a

def ids_admins():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM admins')
    idin = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    a = []
    for i in idin:
        a.append(i[0])
    return a

def delete_admin(username,nick_name ):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM admins WHERE username=:username AND nick_name=:nick_name',
                   {'nick_name':nick_name, 'username':username})
    conn.commit()
    cursor.close()
    conn.close()

def add_robber_id(id, username):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    if username == None:
        username = 'None'
    cursor.execute('INSERT INTO robers (id, username) VALUES (?, ?)', (id, '@'+ username))
    conn.commit()
    cursor.close()
    conn.close()

def save_discription(texts):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE robers SET description=:description WHERE is_on=:is_on', {'is_on': 'None', 'description': texts})
    conn.commit()
    cursor.close()
    conn.close()

def save_photo(texts):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE robers SET photo=:photo WHERE is_on=:is_on', {'is_on': 'None', 'photo': texts})
    conn.commit()
    cursor.close()
    conn.close()

def save_nikcname(texts):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE robers SET nick_name=:nick_name WHERE is_on=:is_on', {'is_on': 'None', 'nick_name': texts})
    conn.commit()
    cursor.close()
    conn.close()

def save_telegr(texts):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE robers SET telegraph=:telegraph WHERE is_on=:is_on', {'is_on': 'None', 'telegraph': texts})
    cursor.execute('UPDATE robers SET is_on=:is_on WHERE is_on=:is_on_', {'is_on_': 'None', 'is_on': 'Not none'})
    conn.commit()
    cursor.close()
    conn.close()

def delete_none_users():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM robers WHERE is_on=:is_on',
                   {'is_on': 'None'})
    conn.commit()
    cursor.close()
    conn.close()

def search_by_name(name):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM robers')
    all_robbers = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    final = []

    for i in all_robbers:
        if name in i[2]:
            final.append(i)

    return final

def search_by_un(name):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM robers')
    all_robbers = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    final = []

    for i in all_robbers:
        if name in i[1]:
            final.append(i)

    return final

def all_info_robbers():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM robers')
    all_robbers = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    final = []

    for i in all_robbers:
        final.append(i)

    return final

def new_user(id):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users')
    all_users = cursor.fetchall()
    final = []
    for i in all_users:
        final.append(i[0])
    if id not in final:
        cursor.execute('INSERT INTO users (id, stat) VALUES (?, ?)', (id, 0))
    else:
        pass
    conn.commit()
    cursor.close()
    conn.close()

def statistics_plus(id):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT stat FROM users WHERE id=:id', {'id':id})
    stat = cursor.fetchone()[0] +1
    cursor.execute('UPDATE users SET stat=:stat WHERE id=:id', {'id': id, 'stat': stat})
    conn.commit()
    cursor.close()
    conn.close()

def statistics_daily():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT stat FROM users')
    all_users = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()

    final = 0
    for i in all_users:
        final += i[0]

    return final

def statistics_registred():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users')
    all_users = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()

    final = []
    for i in all_users:
        final.append(i[0])

    return final

def clear_stat():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET stat=:stat', {'stat', 0})
    conn.commit()
    cursor.close()
    conn.close()


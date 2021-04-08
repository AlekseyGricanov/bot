from connect import connect

conn = connect()
cur = conn.cursor()

def exist(user_id):
    cur.execute("SELECT * FROM users WHERE user_id = %d" % user_id)
    result = cur.fetchone()
    if result is None:
        return False
    return True

def insert_new_user(user_id, user_group):
    cur.execute("INSERT INTO users VALUES (%d, '%s')" % (user_id, user_group))
    conn.commit()
    
def get_user_group(user_id):
    cur.execute("SELECT user_group FROM users WHERE user_id = %d" % user_id)
    result = cur.fetchone()
    return result[0]

def set_user_group(user_id, user_group):
    cur.execute("UPDATE users SET user_group = '%s' WHERE user_id = %d" % (user_group, user_id))
    conn.commit()

def delete_user(user_id):
    cur.execute("DELETE FROM users WHERE user_id=%d" % user_id)
    conn.commit()
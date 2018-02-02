import os
import psycopg2

# get environmental variable from virtual environment
def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


def create_table(db, user, tablename, text_cols):
    # string to create text columns in table
    col_str_root = '{}  TEXT NOT NULL'
    col_str = ', '.join([col_str_root] * len(text_cols)).format(*text_cols)

    # sql string
    sql_str = '''CREATE TABLE {} (id INT PRIMARY KEY  NOT NULL, {})'''

    # open connection and build cursor
    con = None
    con = psycopg2.connect(database=db, user=user)
    cur = con.cursor()

    # add table to the database
    cur.execute(sql_str.format(tablename, col_str))

    # close the connections
    cur.close()
    con.commit()
    con.close()

    return

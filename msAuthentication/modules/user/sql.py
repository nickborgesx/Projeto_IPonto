class SQLUser:
    _TABLE_NAME = "Users"
    _COL_ID = 'id'
    _COL_USERNAME = 'username'
    _COL_PASSWORD = 'password'

    _CREATE_TABLE = (f'CREATE TABLE IF NOT EXISTS {_TABLE_NAME}'
                     f'({_COL_ID} SERIAL PRIMARY KEY,'
                     f'{_COL_USERNAME} VARCHAR(255),'
                     f'{_COL_PASSWORD} VARCHAR(255))')

    _SELECT_ALL = f"SELECT * from {_TABLE_NAME}"
    _SELECT_BY_ID = f'SELECT * from {_TABLE_NAME} WHERE {_COL_ID} = %s'
    _USERS_VALID = f"SELECT * FROM {_TABLE_NAME} WHERE {_COL_USERNAME} = %s AND {_COL_PASSWORD} = %s"
    _PASS_VALID = f'SELECT * from {_TABLE_NAME} WHERE {_COL_PASSWORD} = %s'
    _USER_NAME = f'SELECT * from {_TABLE_NAME} WHERE {_COL_USERNAME} = %s'

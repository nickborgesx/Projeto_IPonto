class SQLUsers:
    _TABLE_NAME = 'Users'
    _COL_ID = 'id'
    _COL_NAME = 'name'
    _COL_PASSWORD = 'password'

    _CREATE_TABLE = f'CREATE TABLE IF NOT EXISTS {_TABLE_NAME}' \
                    f'(id serial primary key, ' \
                    f'{_COL_NAME} varchar(255), ' \
                    f'{_COL_PASSWORD} varchar(255) ' \
                    f');'

    _USERS_VALID = f"SELECT * FROM {_TABLE_NAME} WHERE {_COL_NAME} = %s AND {_COL_PASSWORD} = %s;"
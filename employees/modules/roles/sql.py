class SQLRole:
    _TABLE_NAME = 'roles'
    _COL_ID = 'id'
    _COL_TITLE = 'title'

    _CREATE_TABLE = (f'CREATE TABLE IF NOT EXISTS {_TABLE_NAME}'
                     f'({_COL_ID} SERIAL PRIMARY KEY,'
                     f'{_COL_TITLE} VARCHAR(255));')

    _SELECT_ALL = f"SELECT * from {_TABLE_NAME}"
    _SELECT_BY_ID = f'SELECT * from {_TABLE_NAME} WHERE {_COL_ID} = %s'
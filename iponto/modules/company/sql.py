class SQLCompany:
    _TABLE_NAME = 'company'
    _COL_ID = 'id'
    _COL_NAME = 'name'
    _COL_CNPJ = 'cnpj'
    _COL_LAT = 'lat'
    _COL_LNG = 'lng'
    _CAMPOS_OBRIGATORIOS = [_COL_NAME, _COL_CNPJ, _COL_LAT, _COL_LNG]

    _CREATE_TABLE = (f'CREATE TABLE IF NOT EXISTS {_TABLE_NAME}'
                     f'({_COL_ID} SERIAL PRIMARY KEY,'
                     f'{_COL_NAME} VARCHAR(255),'
                     f'{_COL_CNPJ} VARCHAR(255) UNIQUE,'
                     f'{_COL_LAT} VARCHAR(255),'
                     f'{_COL_LNG} VARCHAR(255));')

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME} ({_COL_NAME}, {_COL_CNPJ}, {_COL_LAT}, {_COL_LNG}) VALUES (%s, %s, %s, %s) RETURNING {_COL_ID};'
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_CNPJ = f'SELECT * FROM {_TABLE_NAME} WHERE {_COL_CNPJ} ILIKE %s'
    _SELECT_BY_ID = f'SELECT * FROM {_TABLE_NAME} WHERE {_COL_ID} = %s'
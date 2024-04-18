class SQLEmployees:
    _TABLE_NAME = 'employee'
    _TABLE_NAME_ROLE = 'roles'
    _COL_ID = 'id'
    _COL_NAME = 'name'
    _COL_CPF = 'cpf'
    _COL_ROLES_ID = 'roles_id'
    _CAMPOS_OBRIGATORIOS = [_COL_NAME, _COL_CPF, _COL_ROLES_ID]

    _CREATE_TABLE = (f'CREATE TABLE IF NOT EXISTS {_TABLE_NAME} '
                     f'({_COL_ID} SERIAL PRIMARY KEY, '
                     f'{_COL_NAME} VARCHAR(255), '
                     f'{_COL_CPF} VARCHAR(255) UNIQUE, '
                     f'{_COL_ROLES_ID} INTEGER REFERENCES {_TABLE_NAME_ROLE}({_COL_ID}));')

    _INSERT_INTO = f'INSERT INTO {_TABLE_NAME} ({_COL_NAME}, {_COL_CPF}, {_COL_ROLES_ID}) VALUES (%s, %s, %s) RETURNING {_COL_ID};'
    _SELECT_ALL = f'SELECT m.{_COL_ID}, m.{_COL_NAME}, d.{_COL_NAME} AS {_TABLE_NAME_ROLE} ' \
                  f'FROM {_TABLE_NAME} m INNER JOIN {_TABLE_NAME_ROLE} d ON m.{_COL_ROLES_ID} = d.{_COL_ID};'
    # _UPDATE_USER = f'UPDATE {_TABLE_NAME} SET {_COL_NAME} = %s, {_COL_PASSWORD} =%s WHERE {_COL_ID} = %s;'
    # _DELETE_USER = f'DELETE FROM {_TABLE_NAME} WHERE {_COL_ID} = %s;'
    # _USERS_VALID = f"SELECT * FROM {_TABLE_NAME} WHERE {_COL_USERNAME} = %s AND {_COL_PASSWORD} = %s;"
    # _SELECT_USER_NAME = f"SELECT * FROM {_TABLE_NAME} WHERE {_COL_NAME} ILIKE %s"
    # _SELECT_ID = f"SELECT id, name, role FROM {_TABLE_NAME} WHERE id = %s"
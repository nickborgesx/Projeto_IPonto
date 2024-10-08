class SQLScale:
    _TABLE_NAME = 'scale'
    _COL_ID = 'id'
    _COL_DATE = 'date'
    _COL_TYPE = 'type'
    _COL_MONTH = 'month'
    _COL_YEAR = 'year'
    _COL_MORNING_BREAK = 'morning_break'
    _COL_AFTERNOON_BREAK = 'afternoon_break'
    _COL_NIGHT_BREAK = 'night_break'
    _COL_EMPLOYEE_ID = 'employee_id'
    _COL_INPUT1 = 'input1'
    _COL_OUTPUT1 = 'output1'
    _COL_INPUT2 = 'input2'
    _COL_OUTPUT2 = 'output2'
    _CAMPOS_OBRIGATORIOS = [_COL_TYPE, _COL_MONTH, _COL_YEAR, _COL_EMPLOYEE_ID]

    _CREATE_TABLE = (f'CREATE TABLE IF NOT EXISTS {_TABLE_NAME} '
                     f'({_COL_ID} SERIAL PRIMARY KEY, '
                     f'{_COL_DATE} VARCHAR(255), '
                     f'{_COL_TYPE} VARCHAR(255), '
                     f'{_COL_MONTH} INT, '
                     f'{_COL_YEAR} INT, '
                     f'{_COL_MORNING_BREAK} VARCHAR(255), '
                     f'{_COL_AFTERNOON_BREAK} VARCHAR(255), '
                     f'{_COL_NIGHT_BREAK} VARCHAR(255), '
                     f'{_COL_INPUT1} VARCHAR(255), '
                     f'{_COL_OUTPUT1} VARCHAR(255), '
                     f'{_COL_INPUT2} VARCHAR(255), '
                     f'{_COL_OUTPUT2} VARCHAR(255), '
                     f'{_COL_EMPLOYEE_ID} INT REFERENCES employee({_COL_ID}));')

    _INSERT_INTO = (f'INSERT INTO {_TABLE_NAME} '
                    f'({{{_COL_TYPE},{_COL_DATE}, {_COL_MONTH}, {_COL_YEAR}, {_COL_MORNING_BREAK}, {_COL_AFTERNOON_BREAK}, '
                    f'{_COL_NIGHT_BREAK}, {_COL_INPUT1}, {_COL_OUTPUT1}, {_COL_INPUT2}, {_COL_OUTPUT2}, {_COL_EMPLOYEE_ID}) '
                    f'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING {_COL_ID};')
    _SELECT_ALL = f'SELECT * FROM {_TABLE_NAME}'
    _SELECT_BY_EMPLOYEE_AND_DATE = f'SELECT * FROM {_TABLE_NAME} WHERE {_COL_EMPLOYEE_ID} = %s AND {_COL_DATE} = %s'
    _SELECT_BY_DATE_AND_EMPLOYEE_ID = f'SELECT s.{_COL_ID},s.{_COL_DATE},s.{_COL_TYPE},s.{_COL_MONTH},s.{_COL_YEAR},s.{_COL_MORNING_BREAK},s.{_COL_AFTERNOON_BREAK},s.{_COL_NIGHT_BREAK},s.{_COL_INPUT1},s.{_COL_OUTPUT1},s.{_COL_INPUT2},s.{_COL_OUTPUT2},e."name" FROM {_TABLE_NAME} s JOIN "employee" e ON s.{_COL_EMPLOYEE_ID} = e.{_COL_ID} WHERE {_COL_DATE} = %s AND {_COL_EMPLOYEE_ID} = %s'
    _UPDATE_INPUT1 = f'UPDATE {_TABLE_NAME} SET {_COL_INPUT1} = %s WHERE {_COL_DATE} = %s AND {_COL_EMPLOYEE_ID} = %s'
    _UPDATE_EXIT1 = f'UPDATE {_TABLE_NAME} SET {_COL_OUTPUT1} = %s WHERE {_COL_DATE} = %s AND {_COL_EMPLOYEE_ID} = %s'
    _UPDATE_INPUT2 = f'UPDATE {_TABLE_NAME} SET {_COL_INPUT2} = %s WHERE {_COL_DATE} = %s AND {_COL_EMPLOYEE_ID} = %s'
    _UPDATE_EXIT2 = f'UPDATE {_TABLE_NAME} SET {_COL_OUTPUT2} = %s WHERE {_COL_DATE} = %s AND {_COL_EMPLOYEE_ID} = %s'
    _SELECT_INPUT_EXIT = f'SELECT s.{_COL_ID}, s.{_COL_DATE}, s.{_COL_MONTH}, s.{_COL_YEAR}, s.{_COL_INPUT1}, s.{_COL_OUTPUT1}, s.{_COL_INPUT2}, s.{_COL_OUTPUT2}, e.name FROM {_TABLE_NAME} s JOIN employee e ON s.{_COL_EMPLOYEE_ID} = e.{_COL_ID} WHERE {_COL_MONTH} = %s AND {_COL_YEAR} = %s AND {_COL_EMPLOYEE_ID} = %s AND (({_COL_INPUT1} IS NOT NULL AND {_COL_OUTPUT1} IS NOT NULL) OR ({_COL_INPUT2} IS NOT NULL AND {_COL_OUTPUT2} IS NOT NULL))'
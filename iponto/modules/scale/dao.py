from iponto.modules.scale.sql import SQLScale
from iponto.modules.scale.modelo import Scale
from iponto.service.connect import Connect

class DAOScale(SQLScale):
    def __init__(self):
        self.connection = Connect().get_instance()

    def create_table(self):
        return self._CREATE_TABLE

    def create_table(self):
        return self._CREATE_TABLE

    def salvar(self, scale: Scale):
        query = (f'INSERT INTO {SQLScale._TABLE_NAME} '
                 f'({SQLScale._COL_TYPE}, {SQLScale._COL_MONTH}, {SQLScale._COL_YEAR}, '
                 f'{SQLScale._COL_DATE}, {SQLScale._COL_MORNING_BREAK}, {SQLScale._COL_AFTERNOON_BREAK}, '
                 f'{SQLScale._COL_NIGHT_BREAK}, {SQLScale._COL_INPUT1}, {SQLScale._COL_EXIT1}, '
                 f'{SQLScale._COL_INPUT2}, {SQLScale._COL_EXIT2}, {SQLScale._COL_EMPLOYEE_ID}) '
                 f'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING {SQLScale._COL_ID};')

        cursor = self.connection.cursor()
        cursor.execute(query, (
            scale.type, scale.month, scale.year, scale.date,
            scale.morning_break, scale.afternoon_break, scale.night_break,
            scale.input1, scale.exit1, scale.input2, scale.exit2,
            scale.employee_id
        ))
        scale_id = cursor.fetchone()[0]
        scale.id = scale_id
        self.connection.commit()
        return scale

    def get_by_employee_and_date(self, employee_id, date):
        query = self._SELECT_BY_EMPLOYEE_AND_DATE
        cursor = self.connection.cursor()
        cursor.execute(query, (employee_id, date))
        result = cursor.fetchone()
        if result:
            cols = [desc[0] for desc in cursor.description]
            scale_dict = dict(zip(cols, result))
            return Scale(**scale_dict)
        else:
            return None
from iponto.modules.scale.sql import SQLScale
from iponto.modules.scale.modelo import Scale
from iponto.service.connect import Connect

class DAOScale(SQLScale):
    def __init__(self):
        self.connection = Connect().get_instance()

    def create_table(self):
        return self._CREATE_TABLE

    def salvar(self, scale: Scale):
        if scale.id:
            return self.atualizar(scale)
        else:
            return self.inserir(scale)

    def inserir(self, scale: Scale):
        query = (f'INSERT INTO {SQLScale._TABLE_NAME} '
                 f'({SQLScale._COL_TYPE}, {SQLScale._COL_MONTH}, {SQLScale._COL_YEAR}, '
                 f'{SQLScale._COL_DATE}, {SQLScale._COL_MORNING_BREAK}, {SQLScale._COL_AFTERNOON_BREAK}, '
                 f'{SQLScale._COL_NIGHT_BREAK}, {SQLScale._COL_INPUT1}, {SQLScale._COL_OUTPUT1}, '
                 f'{SQLScale._COL_INPUT2}, {SQLScale._COL_OUTPUT2}, {SQLScale._COL_EMPLOYEE_ID}) '
                 f'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING {SQLScale._COL_ID};')

        cursor = self.connection.cursor()
        cursor.execute(query, (
            scale.type, scale.month, scale.year, scale.date,
            scale.morning_break, scale.afternoon_break, scale.night_break,
            scale.input1, scale.output1, scale.input2, scale.output2,
            scale.employee_id
        ))
        scale_id = cursor.fetchone()[0]
        scale.id = scale_id
        self.connection.commit()
        return scale

    def atualizar(self, scale: Scale):
        query = (f'UPDATE {SQLScale._TABLE_NAME} SET '
                 f'{SQLScale._COL_TYPE} = %s, {SQLScale._COL_MONTH} = %s, '
                 f'{SQLScale._COL_YEAR} = %s, {SQLScale._COL_DATE} = %s, '
                 f'{SQLScale._COL_MORNING_BREAK} = %s, {SQLScale._COL_AFTERNOON_BREAK} = %s, '
                 f'{SQLScale._COL_NIGHT_BREAK} = %s, {SQLScale._COL_INPUT1} = %s, '
                 f'{SQLScale._COL_OUTPUT1} = %s, {SQLScale._COL_INPUT2} = %s, '
                 f'{SQLScale._COL_OUTPUT2} = %s '
                 f'WHERE {SQLScale._COL_ID} = %s;')

        cursor = self.connection.cursor()
        cursor.execute(query, (
            scale.type, scale.month, scale.year, scale.date,
            scale.morning_break, scale.afternoon_break, scale.night_break,
            scale.input1, scale.output1, scale.input2, scale.output2,
            scale.id
        ))
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

    def atualizar_ponto(self, escala, horario):
        if escala.input1 is None:
            escala.input1 = horario
        elif escala.output1 is None:
            escala.output1 = horario
        elif escala.input2 is None:
            escala.input2 = horario
        elif escala.output2 is None:
            escala.output2 = horario

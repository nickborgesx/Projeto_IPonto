class Scale:
    def __init__(self, type, month, year, morning_break, afternoon_break, night_break, employee_id, input1=None, exit1=None, input2=None, exit2=None, id=None, date=None):
        self.id = id
        self.date = date
        self.type = type
        self.month = month
        self.year = year
        self.morning_break = morning_break
        self.afternoon_break = afternoon_break
        self.night_break = night_break
        self.employee_id = employee_id
        self.input1 = input1
        self.exit1 = exit1
        self.input2 = input2
        self.exit2 = exit2

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type,
            'month': self.month,
            'year': self.year,
            'morning_break': self.morning_break,
            'afternoon_break': self.afternoon_break,
            'night_break': self.night_break,
            'employee_id': self.employee_id,
            'input1': self.input1,
            'exit1': self.exit1,
            'input2': self.input2,
            'exit2': self.exit2
        }

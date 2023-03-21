class ColumnTablePair:
    def __init__(self, table, column):
        self.column = column
        self.table = table
        self.purposes = []

    def __eq__(self, other):
        return self.column == other.column and self.table == other.table

    def __repr__(self):
        return self.table + ":" + self.column

    def add_purpose(self, purpose):
        if purpose not in self.purposes:
            self.purposes.append(purpose)

    def get_purposes_with_legal_reason(self):
        output = []
        for purpose in self.purposes:
            if purpose.legally_required == 1:
                output.append(purpose)
        return output

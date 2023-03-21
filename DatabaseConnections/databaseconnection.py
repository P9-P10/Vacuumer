class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None

    def run_query(self, query):
        pass

    def run_script(self, query):
        pass

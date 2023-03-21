class Purpose:
    def __init__(self, purpose, ttl, origin, start_time, legally_required):
        self.legally_required = legally_required
        self.start_time = start_time
        self.origin = origin
        self.ttl = ttl
        self.purpose = purpose

    def __repr__(self):
        return self.purpose

    def __eq__(self, other):
        return self.purpose == other.purpose \
            and self.ttl == other.ttl \
            and self.start_time == other.start_time \
            and self.legally_required == other.legally_required \
            and self.origin == other.origin

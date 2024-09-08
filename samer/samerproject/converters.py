class ObjectIdConverter:
    regex = "[0-9a-f]{24}"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value

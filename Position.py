class Position:
    def __init__(self,type,name,description,value = None):
        self.type = type
        self.name = name
        self.description = description
        self.value = value

class SelectPosition:
    def __init__(self,name,description,content,value = None,type = 'select'):
        self.type = type
        self.name = name
        self.description = description
        self.value = value
        self.content= content
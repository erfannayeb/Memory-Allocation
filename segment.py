class Segment:
    def __init__(self, seg_id, base_addr=0, limit=0, end_time=-1, num_page=0):
        self.__id = seg_id
        self.__base_addr = base_addr
        self.__limit = limit
        self.__end_time = end_time
        self.__num_page = num_page

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def base_addr(self):
        return self.__base_addr

    @base_addr.setter
    def base_addr(self, value):
        self.__base_addr = value

    @property
    def limit(self):
        return self.__limit

    @limit.setter
    def limit(self, value):
        self.__limit = value

    @property
    def end_time(self):
        return self.__end_time

    @end_time.setter
    def end_time(self, value):
        self.__end_time = value

    @property
    def num_page(self):
        return self.__num_page

    @num_page.setter
    def num_page(self, value):
        self.__num_page = value    

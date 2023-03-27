class Page:
    count = 0

    def __init__(self, seg_id, frame_id, end_time=-1):
        self.__id = seg_id
        self.__page_id, = Page.count,
        self.__frame_id = frame_id
        self.__end_time = end_time
        Page.count += 1

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def page_id(self):
        return self.__page_id

    @page_id.setter
    def page_id(self, value):
        self.__page_id = value

    @property
    def frame_id(self):
        return self.__frame_id

    @frame_id.setter
    def frame_id(self, value):
        self.__frame_id = value

    @property
    def end_time(self):
        return self.__end_time

    @end_time.setter
    def end_time(self, value):
        self.__end_time = value

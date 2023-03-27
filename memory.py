class Memory:
    def __init__(self, user_space, os_space):
        self.__user_space = user_space
        self.__os_space = os_space

    @property
    def user_space(self):
        return self.__user_space

    @user_space.setter
    def user_space(self, value):
        self.__user_space = value

    @property
    def os_space(self):
        return self.__os_space

    @os_space.setter
    def os_space(self, value):
        self.__os_space = value

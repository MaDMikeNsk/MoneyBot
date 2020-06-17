class Statement:
    def __init__(self):
        self.__statement = {'ch_active': False,
                          'ch_info': None,
                          'post_active': False,
                          'post_info': None,
                          'link_active': False,
                          'link_info': None}

    # ==================================================================================================================
    #                                                   SETTERS
    # ==================================================================================================================
    def set_statement(self, ch=None, post=None, link=None):
        if ch:
            self.__statement['ch_active'] = True
            self.__statement['ch_info'] = ch
        if post:
            self.__statement['post_active'] = True
            self.__statement['post_info'] = post
        if link:
            self.__statement['link_active'] = True
            self.__statement['link_info'] = link

    def set_post_starttime(self, st):
        self.__statement['post_info']['start_time'] = st

    def set_1stage_link_starttime(self, st):
        self.__statement['link_info']['start_time'] = st

    # ==================================================================================================================
    #                                                  GETTERS
    # ==================================================================================================================
    def get_ch_info(self):
        return self.__statement['ch_info']

    def get_post_info(self):
        return self.__statement['post_info']

    def get_link_info(self):
        return self.__statement['link_info']

    # ==================================================================================================================
    #                                               IS TASK ACTIVE
    # ==================================================================================================================
    def is_channel_active(self):
        return self.__statement['ch_active']

    def is_post_active(self):
        return self.__statement['post_active']

    def is_link_active(self):
        return self.__statement['link_active']

    # ==================================================================================================================
    #                                               RESET STATEMENT
    # ==================================================================================================================
    def reset_statement(self, ch=None, post=None, link=None):
        if ch == 'zero':
            self.__statement['ch_active'] = False
            self.__statement['ch_info'] = None
        if post == 'zero':
            self.__statement['post_active'] = False
            self.__statement['post_info'] = None
        if link == 'zero':
            self.__statement['link_active'] = False
            self.__statement['link_info'] = None

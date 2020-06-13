class Statement:
    def __init__(self):
        self.statement = {'ch_active': False,
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
            self.statement['ch_active'] = True
            self.statement['ch_info'] = ch
        if post:
            self.statement['post_active'] = True
            self.statement['post_info'] = post
        if link:
            self.statement['link_active'] = True
            self.statement['link_info'] = link

    def set_post_starttime(self, st):
        self.statement['post_info']['start_time'] = st

    def set_1stage_link_starttime(self, st):
        self.statement['link_info']['start_time'] = st

    # ==================================================================================================================
    #                                                  GETTERS
    # ==================================================================================================================
    def get_ch_info(self):
        return self.statement['ch_info']

    def get_post_info(self):
        return self.statement['post_info']

    def get_link_info(self):
        return self.statement['link_info']

    # ==================================================================================================================
    #                                               IS TASK ACTIVE
    # ==================================================================================================================
    def is_channel_active(self):
        return self.statement['ch_active']

    def is_post_active(self):
        return self.statement['post_active']

    def is_link_active(self):
        return self.statement['link_active']

    # ==================================================================================================================
    #                                               RESET STATEMENT
    # ==================================================================================================================
    def reset_statement(self, ch=None, post=None, link=None):
        if ch == 'zero':
            self.statement['ch_active'] = False
            self.statement['ch_info'] = None
        if post == 'zero':
            self.statement['post_active'] = False
            self.statement['post_info'] = None
        if link == 'zero':
            self.statement['link_active'] = False
            self.statement['link_info'] = None

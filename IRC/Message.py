#
# Message.py
#
# Created on: October 13, 2012
#     Author: Todd Lunter
#

import re

class Message(object):
    """
    A standard IRC message object that will store the message details.

    Class attribute:
        `_regex`: keeps track of how to parse each message.

    Attributes:
        `raw_msg`: Given raw message
        `username`: Parsed out username
        `hostname`: Parsed out hostname
        `action`: Parsed out action
        `channel`: Parsed out channel
        `msg`: Parsed out message
    """
    _regex = r':((?P<USERNAME>[^!]+)!)?(?P<HOSTNAME>\S+)\s+(?P<ACTION>\S+)\s+:?(?P<CHANNEL>\S+)\s*(?:(?::|[+-]+)(?P<MESSAGE>.*))?'

    def __init__(self, username=None, hostname=None, action=None,
                 channel=None, msg=None):
        """Inits an IRC Message"""

        self.raw_msg = ""
        self.username = username or ""
        self.hostname = hostname or ""
        self.action = action or ""
        self.channel = channel or ""
        self.msg = msg or ""

    def __repr__(self):
        return "Message(username=%r, hostname=%r, action=%r, channel=%r, msg=%r)" % (
                self.username, self.hostname, self.action, self.channel, self.msg)

    def __eq__(self, other):
        return (self.username == other.username and
                self.hostname == other.hostname and
                self.action == other.action and
                self.channel == other.channel and
                self.msg == other.msg)

    def __hash__(self):
        hashables = (self.username, self.hostname, self.action,
                     self.channel, self.msg)

        result = 0
        for value in hashables:
            result = 33*result + hash(value)
        return hash(result)

    @classmethod
    def from_string(cls, raw_string):
        """Inits a message with the given raw_string"""
        msg = Message()
        msg.raw_msg = raw_string
        matches = re.match(Message._regex, msg.raw_msg)
        
        if matches:
            matches_dict = matches.groupdict()
            msg.username = matches_dict['USERNAME'] or ""
            msg.hostname = matches_dict['HOSTNAME'] or ""
            msg.action = matches_dict['ACTION'] or ""
            msg.channel = matches_dict['CHANNEL'] or ""
            msg.msg = matches_dict['MESSAGE'] or ""

        return msg

    def to_raw(self, with_username=None):
        string_list = []

        if with_username == True and len(self.hostname) > 0:
            string_list.append(':')
            if len(self.username) > 0:
                string_list.append(self.username)
                string_list.append('!')

            string_list.append(self.hostname)
            string_list.append(' ')

        string_list.append(self.action)
        string_list.append(' ')
        string_list.append(self.channel)
        string_list.append(' :')
        string_list.append(self.msg)

        self.raw_msg = ''.join(string_list)
        
        return self.raw_msg


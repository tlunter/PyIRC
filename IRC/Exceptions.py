#
# Exceptions.py
#
#  Created on: October 20, 2012
#      Author: Todd Lunter
#

class IRCError(Exception):
    """Base IRC Class exception"""
    pass

class MessageSendError(IRCError):
    """An error occured while trying to send a message"""
    pass

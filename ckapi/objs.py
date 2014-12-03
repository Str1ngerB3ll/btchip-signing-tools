#
# Wrappers for Coinkite objects which you might see.
#
# Full docs at: https://docs.coinkite.com/
# 
# Copyright (C) 2014 Coinkite Inc. (https://coinkite.com) ... See LICENSE.md
#
import re
from dateutil.parser import parse as iso_parse

CK_DB_OBJECTS = [
    'CKUser', 'CKEvent', 'CKUserRequest', 'CKCard', 'CKActivityLog', 'CKMagicCoin',
    'CKEmailAddress', 'CKInvoice', 'CKReqSend', 'CKAccount', 'CKReqReceive',
    'CKMembershipLevel', 'CKPublicTxn', 'CKBlockInfo', 'CKTxnOutput', 'CKReqTransfer',
    'CKBillPay', 'CKEmailMessage', 'CKTerminal', 'CKTerminalLog', 'CKVoucher', 'CKNotification',
    'CKInvoiceState', 'CKForwarding', 'CKRevenuePayout', 'CKRevShareLink', 'CKRevShareHit',
    'CKPhoneNumber', 'CKSMSMessage', 'CKApiKey'
]

__all__ = CK_DB_OBJECTS + ['CKObject', 'CKDBObject']

class CKObject(dict):
    '''
        Act like a dictionary, but also an object. Keys are attributes, attributes
        are keys and so on.
    '''

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError('No such attribute: %s\nKnown attrs: %s' 
                                        % (name, ', '.join(self.keys())))

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

    def __repr__(self):
        ret =  '<%s:' % self.__class__.__name__
        for k,v in self.items():
            ret += ' %s=%r' % (k, v)
        return ret + '>'

class CKDBObject(CKObject):
    "This object is a proxy for a database object in Coinkite"
    _CK_type = None

    @property
    def ref_number(self):
        return self.CK_refnum

    def for_json(self):
        # useful when used as a argument to another API call.
        return self.ref_number

    def __repr__(self):
        ret =  '<%s:' % self.get('CK_type', self._CK_type or self.__class__.__name__)
        for k,v in self.items():
            ret += ' %s=%r' % (k, v)
        return ret + '>'

# This pattern should match the dates and times from Coinkite server
# for the next 80 years or so.
DATETIME_RE = re.compile(r'^20\d\d-\d\d-\d\dT\d\d:\d\d:\d\d.\d+(Z|)$')

def make_db_object(d):
    # Given a dict straight from the JSON, return a more functional object
    # which maybe a proxy or wrapper version object.
    #
    cls = d.get('CK_type', None)

    # Look for ISO datetimes. This is a little risky, but I know about the
    # server we're talking with, so...
    #
    # example:      2014-07-07T18:48:34.880819
    #
    for k, v in d.items():
        if isinstance(v, basestring) and DATETIME_RE.match(v):
            try:
                d[k] = iso_parse(v)
            except:
                pass

    if not cls or cls not in CK_DB_OBJECTS:
        return CKObject(d)

    # Return a CKUser (for example) if the incoming data looks like one
    return globals()[cls](d)

# Declare a trival subclass of CKDBObject() for each of those names.
#
def onetime_setup():
    for _name in CK_DB_OBJECTS:
        _a = dict(CKDBObject.__dict__)
        _a['_CK_type'] = _name
        globals()[_name] = type(_name, (CKDBObject,), _a)

# I like clean namespaces
onetime_setup()
del onetime_setup

# EOF


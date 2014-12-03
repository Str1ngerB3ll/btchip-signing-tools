#
# Coinkite API: Make requests of the API easily.
#
# Full docs at: https://docs.coinkite.com/
# 
# Copyright (C) 2014 Coinkite Inc. (https://coinkite.com) ... See LICENSE.md
# 
#
import logging
from objs import make_db_object
from decimal import Decimal

try:
    # We prefer simple json.
    import simplejson

    json_encoder = simplejson.JSONEncoder(use_decimal=True, for_json=True)
    json_decoder = simplejson.JSONDecoder(object_hook=make_db_object, parse_float=Decimal)

except ImportError:
    # We need Decimal to be encoded corrected both for read and write! Not simple.
    import json
    json_decoder = json.JSONDecoder(object_hook=make_db_object, parse_float=Decimal)

    # Lessons learned from http://stackoverflow.com/questions/1960516
    # - the provided API is not suffient to do Decimal in place of float
    # - monkey patching is too version sensitive
    # - the code in json.encoding is too heavy-duty to patch
    # - it can't be done, just use SimpleJSON
    #
    class DecimalEncoder(json.JSONEncoder):

        def default(self, o):
            if hasattr(o, 'for_json'):
                return o.for_json()

            if isinstance(o, Decimal):
                # NOTE: there is no way to do this better. I've tried. Get SimpleJSON!!
                # This hack will not work for all values!
                f = float(o)
                assert str(f) == str(o)[0:len(str(f))] or int(f) == int(o), (f, o)
                return f

            return json.JSONEncoder.default(self, o)

    json_encoder = DecimalEncoder()


def test_json_encoding():
    # Verify code above is working. Will fail on our hack since it can't
    # represent all these digits.

    a = Decimal('0.3333333333333333333333333333')
    
    enc = json_encoder.encode(a)
    assert enc == '0.3333333333333333333333333333', enc

    aa = json_decoder.decode(enc)
    assert a == aa, aa

    enc = json_encoder.encode(dict(test=a))
    dd = json_decoder.decode(enc)
    assert dd == dict(test=a)



# EOF

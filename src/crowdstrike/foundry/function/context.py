from contextvars import ContextVar

# While this holds the inbound handler request, do not access them directly
# without good reason.  This is intended for those situations in which
# it is not possible to pass the inbound request around the handler via method
# arguments, such as in logging.

# Holds the inbound handler request after the payload has been converted from
# a dict to a Request.
ctx_request = ContextVar('request', default=None)

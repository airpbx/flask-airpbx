#
# Flask-Airpbx
#
# Copyright (C) 2021 Airpbx Ltd
# All rights reserved
#


from flask.signals import Namespace


namespace = Namespace()

ping = namespace.signal('ping')


# EOF

#!/usr/bin/env python
#
#  Copyright (c) 2013, Corey Goldberg (cgoldberg@gmail.com)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  Requires: Python 2.7/3.2+


from order.uob import  *
from session.session import Session


if __name__ == '__main__':
	print "s"
	print UOB_USERNAME
	print UOB_PASSWORD
	session = Session()
	session.Login("UOB")

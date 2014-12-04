# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

"""gGRC-Core extension lookup. Taken after the approach used in Flask for
providing an automated way to perform extension module lookup.
"""

def setup():
  from flask.exthook import ExtensionImporter
  importer = ExtensionImporter(['ggrc_%s', 'ggrcext.%s'], __name__)
  importer.install()

setup()
del setup


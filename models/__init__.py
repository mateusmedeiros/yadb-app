# Taken from essentialcode.com, based on a init.py file from Google for a tests module.
# for more info: http://www.essentialcode.com/2009/01/26/splitting-django-models-into-separate-files/

import os
import re
import types
import unittest
from django.db import models

PACKAGE = '{{ app_name }}.models'
MODEL_RE = r"^.*.py$"

# Search through every file inside this package.
model_names = []
model_dir = os.path.dirname( __file__)
for filename in os.listdir(model_dir):
  if not re.match(MODEL_RE, filename) or filename == "__init__.py":
    continue
  # Import the model file and find all clases inside it.
  model_module = __import__('%s.%s' % (PACKAGE, filename[:-3]),
                           {}, {},
                           filename[:-3])
  for name in dir(model_module):
    item = getattr(model_module, name)
    if not isinstance(item, (type, types.ClassType)):
      continue
    # Found a model, bring into the module namespace.
    exec "%s = item" % name
    model_names.append(name)

# Hide everything other than the classes from other modules.
__all__ = model_names


# Don't forget to add to each model
#
# class Meta:
#     """Meta Class for your model."""
#     app_label = '{{ app_name }}'

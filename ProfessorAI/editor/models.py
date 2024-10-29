from django.db import models
from . import utils

# Create your models here.
db_handle = utils.get_db_handle('customerData')
customers = db_handle['customers']
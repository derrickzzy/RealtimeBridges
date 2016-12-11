import os
from server.models import Bridge

# check if bridge directory exist
def checkdir(bridgenumber):
    if Bridge.objects.filter(number=bridgenumber).exists():
        directory = './EventData/%s' % bridgenumber
        if not os.path.exists(directory):
            os.makedirs(directory)
        tempdir = directory + '/temp/'
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)
        staticdirectory = '/RealtimeBridge/static/%s' % bridgenumber
        if not os.path.exists(staticdirectory):
            os.makedirs(staticdirectory)
        return directory

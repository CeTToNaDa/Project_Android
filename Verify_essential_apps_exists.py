from common import *

unlock_phone()
notFoundApps = []
for app in all_Aps:
    open_app_from_menu(app)

go_home()
testResultMessage()
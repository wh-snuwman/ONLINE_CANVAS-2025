from datetime import datetime
def printlog(type, msg):
    now = datetime.now()
    print(f'[{type}][{now.strftime('%Y-%m-%d %H:%M:%S')}] {msg}')
    return f'[{type}][{now.strftime('%Y-%m-%d %H:%M:%S')}] {msg}'
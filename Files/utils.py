def banned(uid):
    try:
        return True if uid in [int(fuid) for fuid in open('Files/banlist.txt').readlines()] else False
    except Exception as err:
        print(err)


def ban(uid):
    with open('Files/banlist.txt', 'a') as fl:
        fl.write(str(uid) + '\n')

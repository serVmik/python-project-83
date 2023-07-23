url_too_long = '''https://itistooooooooooooooooooooooooooooooooooooooooooooooo
oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
ooooooooooooooooooooooooolongurl.com'''

urls_incorrect = ('htp://sorry.jo', 'http;//just_do.it', 'http://benq,ru')


def give_one_by_one(func):
    def wrapper(*args):
        for arg in args:
            func(arg)
    return wrapper

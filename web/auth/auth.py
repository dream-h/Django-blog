from django.shortcuts import redirect


def check_login(func):
    """
    检查用户是否登录的装饰器
    :param func:
    :return:
    """
    def inner(request, *args, **kwargs):
        if request.session.get('user_info'):
            return func(request, *args, **kwargs)
        else:
            return redirect('/')
    return inner

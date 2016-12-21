from django.contrib.auth.decorators import login_required
from ..pypi_ui.shortcuts import render

def _administrator_required(func):
    @login_required
    def _decorator(request, *args, **kwargs):
        if not request.user.is_staff:
            return render(request, 'pypi_manage/forbidden.html')
        return func(request, *args, **kwargs)
    return _decorator

@_administrator_required
def index(request):
    return render(request, 'pypi_manage/index.html')

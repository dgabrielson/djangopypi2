#######################
from __future__ import unicode_literals, print_function
#######################
from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from ..pypi_ui.shortcuts import render
from ..pypi_packages.models import Package
from ..pypi_packages.models import Release
from .models import MirrorSite
from . import xmlrpc_views
from . import distutils_request

@csrf_exempt
def index(request):
    """ Root view of the package index, handle incoming actions from distutils
    or redirect to a more user friendly view """
    if xmlrpc_views.is_xmlrpc_request(request):
        return xmlrpc_views.handle_xmlrpc_request(request)

    if distutils_request.is_distutils_request(request):
        return distutils_request.handle_distutils_request(request)

    return HttpResponseRedirect(reverse('djangopypi2-packages-index'))

class SimpleIndex(ListView):
    model = Package
    template_name = 'pypi_frontend/package_list_simple.html'
    context_object_name = 'packages'

def _mirror_if_not_found(proxy_folder):
    def decorator(func):
        def internal(request, package_name):
            try:
                return func(request, package_name)
            except Http404:
                for mirror_site in MirrorSite.objects.filter(enabled=True):
                    url = '/'.join([mirror_site.url.rstrip('/'), proxy_folder, package_name])
                    mirror_site.logs.create(action='Redirect to ' + url)
                    return HttpResponseRedirect(url)
            raise Http404(u'%s is not a registered package' % (package_name,))
        return internal
    return decorator

@_mirror_if_not_found('simple')
def simple_details(request, package_name):
    try:
        package = Package.objects.get(name__iexact=package_name)
    except Package.DoesNotExist:
        package = get_object_or_404(Package, name__iexact=package_name.replace('_', '-'))
    # If the package we found is not exactly the same as the name the user typed, redirect
    # to the proper url:
    if package.name != package_name:
        return HttpResponseRedirect(reverse('djangopypi2-simple-package-info', kwargs=dict(package_name=package.name)))
    return render(request, 'pypi_frontend/package_detail_simple.html',
                              context=dict(package=package),
                              content_type='text/html')

@_mirror_if_not_found('pypi')
def package_details(request, package_name):
    package = get_object_or_404(Package, name=package_name)
    return HttpResponseRedirect(package.get_absolute_url())

@_mirror_if_not_found('pypi')
def package_doap(request, package_name):
    package = get_object_or_404(Package, name=package_name)
    return render(request, 'pypi_frontend/package_doap.xml',
                              context=dict(package=package),
                              content_type='text/xml')

def release_doap(request, package_name, version):
    release = get_object_or_404(Release, package__name=package_name, version=version)
    return render(request, 'pypi_frontend/release_doap.xml',
                              context=dict(release=release),
                              content_type='text/xml')

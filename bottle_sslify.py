# -*- coding: utf-8 -*-
__version__ = '0.0.1'
__author__ = 'Ali Yahya'
__email__ = 'alive@athena.ai'


from bottle import hook, redirect, request

class SSLify(object):
  
  def __init__(self, app, permanent=False):
    self.app = app
    self.permanent = permanent

    before_request_decorator = self.app.hook('before_request')
    before_request_decorator(self.https_redirect)
    before_request_decorator(self.url_scheme) # Must come after https_redirect hook


  def https_redirect(self):
    '''Redirect incoming HTTPS requests to HTTPS'''

    forwarded_protocol = request.get_header('X-Forwarded-Proto', '').lower()

    if forwarded_protocol != 'https' and request.url.startswith('http://'):
      url = request.url.replace('http://', 'https://', 1)
      code = 301 if self.permanent else 302

      redirect(url, code=code)

  def url_scheme(self):
    '''Set the URL scheme to https'''
    request.environ['wsgi.url_scheme'] = 'https'

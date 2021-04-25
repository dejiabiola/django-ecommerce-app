import urllib
from urllib.parse import urljoin, urlparse
from behave import given, when, then, model
from django.conf import settings
from django.shortcuts import resolve_url


@given(u'we want to login a user')
def navigate_to_login(context):
  base_url = urllib.request.url2pathname(context.test_case.live_server_url)
  open_url = urljoin(base_url,'/login/')
  context.browser.get(open_url)


@when(u'we fill in the login form with correct data')
def add_login_details(context):
  name_textfield = context.browser.find_element_by_name('username')
  name_textfield.send_keys('username')
  password_textfield = context.browser.find_element_by_name('password')
  password_textfield.send_keys('password')
  context.browser.find_element_by_name('submit').click()


@then(u'it succeeds by navigating to product')
def login_fail(context):
  assert 'Username' in context.browser.page_source
  # print(context.browser.page_source)


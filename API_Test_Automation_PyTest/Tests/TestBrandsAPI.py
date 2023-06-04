import json

import requests
from TestLoginAPI import *

http.client._MAXHEADERS = 1000
config = ConfigParser()
config.read("..\\Config")
configuration = config["Default"]

access_token = test_post_authentication_token_on_login_page()
response = test_get_account_otp_auth_on_login_page(access_token)
time.sleep(10)
otp2 = read_email_from_gmail(email_user, email_password)
updated_access_token = test_post_login_on_login_page(otp2)
anti_forgery_token_sso = test_get_anti_forgery_token_sso_on_login_page(updated_access_token)
anti_forgery_token = test_get_anti_forgery_token_on_login_page(access_token)


def test_get_brands_on_brands_page():
    url1 = configuration['disputedevapiurl'] + "/api/brand"
    headers = {
        'Authorization': ('Bearer ' + updated_access_token)
    }
    response1 = requests.get(url1, headers=headers)
    assert response1.status_code == 200, 'Status Code is not 200 for test_get_brands_on_brands_page'


def test_get_brands_page_on_brands_page():
    url2 = configuration['disputedevurl'] + "/backoffice/app/views/settings/brands.html"
    headers = {
        'Authorization': ('Bearer ' + updated_access_token)
    }
    response2 = requests.get(url2, headers=headers)
    assert response2.status_code == 200, 'Status Code is not 200 for test_get_brands_page_on_brands_page'


def test_get_brands_editor_dialog_on_brands_page():
    url3 = configuration['disputedevurl'] + "/backoffice/app/views/settings/brands.html"
    headers = {
        'Authorization': ('Bearer ' + updated_access_token)
    }
    response3 = requests.get(url3, headers=headers)
    assert response3.status_code == 200, 'Status Code is not 200 for test_get_brands_editor_dialog_on_brands_page'


def test_post_add_brands_on_brands_page():
    # print("Cookie = " + anti_forgery_token[0])
    # print("X-CSRF-Token-SSO = " + anti_forgery_token_sso)
    # print("X-CSRF-Token = " + anti_forgery_token[1])
    url4 = configuration['disputedevapiurl'] + "/api/brand"
    brand = open("..\\TestData\\Brand.json", "r").read()
    brand_json = json.loads(brand)
    headers = {
        'Authorization': ('Bearer ' + updated_access_token),
        'X-CSRF-Token': anti_forgery_token[1],
        'X-CSRF-Token-SSO': anti_forgery_token_sso
    }

    cookies = {
        'Cookie': f'xsrf-token={anti_forgery_token[0]}'
    }
    print(headers)
    print(cookies)
    response4 = requests.post(url4, headers=headers, cookies=cookies, data=brand_json)
    print(response4.content)
    # assert response4.status_code == 200, 'Status Code is not 200 for test_post_add_brands_on_brands_page'


test_get_brands_on_brands_page()
test_get_brands_page_on_brands_page()
test_get_brands_editor_dialog_on_brands_page()
test_post_add_brands_on_brands_page()

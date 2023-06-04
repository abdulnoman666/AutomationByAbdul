import time

import requests
from configparser import ConfigParser
import http.client
from read_email import read_email_from_gmail

http.client._MAXHEADERS = 1000
config = ConfigParser()
config.read("..\\Config")
configuration = config["Default"]
email_user = configuration["emailusername"]
email_password = configuration["emailpassword"]


def test_post_authentication_token_on_login_page():
    params = {
        "grant_type": "password",
        "username": configuration["applicationusername"],
        "password": configuration["applicationpassword"]
    }

    # API URL
    url1 = configuration["finboassourl"] + "/token"
    response1 = requests.post(url1, params)
    assert response1.status_code == 200, "Response code is not 200 for request " + url1
    json_response = response1.json()
    authentication_token = json_response['access_token']
    assert len(authentication_token) >= 283, "Length of Access Token is not greater or Equal to 283"
    assert (json_response['token_type']) == 'bearer', "Token Type is not equal to bearer"
    assert (int(json_response['expires_in'])) == 43199, "Expires_in is not equal to 43199"
    assert (json_response['otp_required']) == 'Please provide otp', "otp_required is not equal to Please provide otp"
    # print(len(access_Token))
    # print(response.headers)
    # print(type(response.headers))
    # print(response.cookies)
    # print(response.encoding)
    # print(response.url)
    return authentication_token


def test_get_account_otp_auth_on_login_page(token):
    url2 = configuration["finboassourl"] + "/api/Account/otp/auth"
    headers = {
        'Authorization': ('Bearer ' + token),
        'Origin': configuration["finboassourl"]
    }
    response2 = requests.get(url2, headers=headers)
    return response2


def test_post_login_on_login_page(otp):
    url3 = configuration["finboassourl"] + "/Token"

    headers = {
        'Origin': configuration["finboassourl"]
    }
    params = {
        "grant_type": "password",
        "username": configuration["applicationusername"],
        "password": configuration["applicationpassword"],
        "scope": f"otp:{otp}"
    }

    response3 = requests.post(url3, params, headers=headers)
    json_response = response3.json()
    assert response3.status_code == 200, 'Status Code is not 200 for test_post_login_on_login_page'
    access_token2 = json_response['access_token']
    assert (json_response['token_type']) == "bearer", 'Token Type is not equal to bearer'
    assert (int(json_response['expires_in'])) == 43199, 'Expires In is not equal to 43199'
    assert (len(access_token2)) >= 368, 'Access Token length is not greater and equal to 368'
    print("Access Token = " + access_token2)
    return access_token2


def test_get_anti_forgery_token_sso_on_login_page(access_token2):
    url4 = configuration['finboassourl'] + "/antiforgerytokensso"
    headers = {
        'Authorization': ('Bearer ' + access_token2)
    }
    response4 = requests.get(url4, headers=headers)
    assert response4.status_code == 200, 'Status Code is not 200 for test_get_anti_forgery_token_sso_on_login_page'
    json_response4 = response4.json()
    print("X-CSRF-Token-SSO = " + json_response4['AntiForgeryToken'])
    assert (len(json_response4['AntiForgeryToken'])) >= 92, "AntiForgery Token length is not greater or equal to 92"
    return json_response4['AntiForgeryToken']


def test_get_anti_forgery_token_on_login_page(access_token2):
    url5 = configuration['disputedevapiurl'] + "/antiforgerytoken"
    headers = {
        'Authorization': ('Bearer ' + access_token2)
    }
    response5 = requests.get(url5, headers=headers)
    assert response5.status_code == 200, 'Status Code is not 200 for test_get_anti_forgery_token_on_login_page'
    # for cookie in response5.cookies:
    #     print("Cookie Name = " + cookie.name + " Cookie Value = " + cookie.value)
    cookie_dict = response5.cookies.get_dict()
    print('Cookie = ' + cookie_dict['xsrf-token'])
    json_response5 = response5.json()
    print('X-CSRF-Token = ' + json_response5['AntiForgeryToken'])
    assert (len(json_response5['AntiForgeryToken'])) >= 92, "AntiForgery Token length is not greater or equal to 92"
    return cookie_dict['xsrf-token'], json_response5['AntiForgeryToken']


# access_token = test_post_authentication_token_on_login_page()
# response = test_get_account_otp_auth_on_login_page(access_token)
# time.sleep(10)
# otp2 = read_email_from_gmail(email_user, email_password)
# updated_access_token = test_post_login_on_login_page(otp2)
# anti_forgery_token_sso = test_get_anti_forgery_token_sso_on_login_page(updated_access_token)
# anti_forgery_token = test_get_anti_forgery_token_on_login_page()

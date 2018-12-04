# 네이버 캡차 API 예제 - 키발급
import urllib.request
import os, sys, ast, json, time, base64, hmac, hashlib

def geoLocation():
    ip = "211.249.69.177"

    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)
    print(timestamp)

    api_key = "inruy633nk"
    access_key = "ACVeW6j6lH7lvswLeo2s"
    secret_key = "kIOm3YHoIiGWTxXSHk3zyrZeZHKWxixzzD8ISG1d"
    secret_key = bytes(secret_key, 'UTF-8')
    method = "GET"

    uri = "/geolocation/v1/geoLocation?ip=" + ip + "&ext=t&responseFormatType=json"
    url = "https://ncloud.apigw.ntruss.com" + uri

    message = method + " " + uri + "\n" + timestamp + "\n" + api_key + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

    sig_key = str(signingKey)
    sig_key = sig_key[2:-1]

    req = urllib.request.Request(url)
    req.add_header("X-ncp-apigw-timestamp", timestamp)
    req.add_header("x-ncp-apigw-api-key", api_key)
    req.add_header("x-ncp-iam-access-key", access_key)
    req.add_header("x-ncp-apigw-signature-v1", sig_key)

    res = urllib.request.urlopen(req)

    rescode = res.getcode()
    if(rescode == 200):
        response_body = res.read()
        response_body = response_body.decode('utf-8')
        # string
        result = response_body
        result = ast.literal_eval(result)
        # dict
        print(response_body)

    else:
        print("Error Code:" + rescode)

geoLocation()

from django.shortcuts import render
from django.http import HttpResponse
from urllib.error import HTTPError, URLError
from django.core.exceptions import ObjectDoesNotExist
import time, base64, hmac, hashlib, ast, os, sys
import urllib.request
from API_List import *
# smtp
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def nameCheck(uri):
    if '/' in uri:
        name = uri.split('/')
        name = name[1]
    elif '?' in  uri:
        name = uri.split('?')
        name = name[0]
    else:
        name = uri
    return str(name)

def auth_Hmac(uri):
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)
    api_key = " API KEY "
    access_key = " ACCESS KEY "
    secret_key = " SECRET KEY "
    secret_key = bytes(secret_key, 'UTF-8')
    method = "GET"
    if uri == '/api-test/v1/api':
        url = "https://ta50do4nv5.apigw.ntruss.com" + uri

    elif uri =='/api/v1/mails/requests/20181022000000073804/status':
        url = "https://mail.apigw.ntruss.com" + uri

    else:
        url = "https://ncloud.apigw.ntruss.com" + uri


    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    sig = "x-ncp-apigw-signature-v2"
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    sig_key = signingKey.decode('utf-8')

    req = urllib.request.Request(url)
    req.add_header("X-ncp-apigw-timestamp", timestamp)
    req.add_header("x-ncp-apigw-api-key", api_key)
    req.add_header("x-ncp-iam-access-key", access_key)
    req.add_header(sig, sig_key)
    return req


def auth_v1(url):
    client_id = ' CLIENT ID'
    client_secret = ' CLIENT SECRET '
    # url = 'https://naveropenapi.apigw.ntruss.com' + url
    req = urllib.request.Request(url)
    req.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    req.add_header("X-NCP-APIGW-API-KEY",client_secret)
    return req


def resCheck(req, i, uri, name, data=''):
    try:
        if i=='captcha':
            res = urllib.request.urlopen(req)
            key = res.read().decode('utf-8')
            key = ast.literal_eval(key)
            client_id = "7gdzqkcoua"
            if uri == '/captcha/v1/nkey?code=0':
                url = "https://naveropenapi.apigw.ntruss.com/captcha-bin/v1/ncaptcha?key=" + key['key'] + "&X-NCP-APIGW-API-KEY-ID=" + client_id
                name = 'imgcaptcha'
            else:
                url = "https://naveropenapi.apigw.ntruss.com/scaptcha-bin/v1/scaptcha?key=" + key['key'] + "&X-NCP-APIGW-API-KEY-ID=" + client_id;
                name = 'audiocaptcha'
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()
            print(f'rescode: {rescode}  name: {name}')
        elif data=='':
            res = urllib.request.urlopen(req)
        else:
            res = urllib.request.urlopen(req, data=data.encode('utf-8'))
    except URLError as e:
        rescode = e
    except HTTPError as e:
        rescode = e
    else:
        rescode = res.getcode()

    type = nameCheck(name)
    type = i + '-' + type
    try:
        slog = NaverApiStatus.objects.get(api_name=type)
    except ObjectDoesNotExist:
        slog = NaverApiStatus(api_type=i, api_name=type, api_status=0, api_time=datetime.datetime.now())

    if(rescode == 200):
        # rtnVal = {'rescode': rescode, 'name': i}
        rtnVal = f'rescode: {rescode}  name: {i}'
        slog.api_time = datetime.datetime.now()
        slog.api_status = 0
        slog.save()
        print(rtnVal)
    else:
        rtnVal = {'rescode': rescode, 'uri': uri + data, 'name': i}
        global count
        if count <= 3 :
            count += 1
            if i in ['clova', 'maps', 'papago', 'nshorturl', 'captcha', 'searchtrend']:
                resCheck(req, i, uri, name, data)
            else:
                resCheck(auth_Hmac(uri), i, uri, name, data)
        else:
            slog.api_status = 1
            slog.save()
            elog = NaverApiErrorLog(api_name=type, api_error_code=rescode, api_error_time=datetime.datetime.now()).save()
            count = 1
            print(rtnVal)
            Mail(rtnVal)


def Mail(rtnVal):
    sender = ' email '
    receivers = [' email ']
    body = f'ErrorCode : {rtnVal["rescode"]}\n\nURI : {rtnVal["uri"]}\n\nName : {rtnVal["name"]}'

    message = MIMEText(str(body))
    message['To'] =  Header(' email ')

    subject = f'{rtnVal["name"]} ERROR'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP(' ip ')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("send mail")
    except smtplib.SMTPException as e:
        print("Mail Error : " + e)


def IaaS(api):
    for i in api:
        for value in api[i].values():
            if i == 'server':
                uri = '/server/v1/' + value
            elif i == 'lb':
                uri = '/loadbalancer/v1/' + value
            elif i == 'autoscaling':
                uri = '/autoscaling/v1/' + value
            elif i == 'monitoring':
                uri = '/monitoring/v1/' + value
            elif i == 'security':
                # uri = '/security/v1/' + value
                continue
            elif i == 'cdn':
                uri = '/cdn/v1/' + value
            elif i == 'clouddb':
                uri = '/clouddb/v1/' + value
            else:
                continue
            resCheck(auth_Hmac(uri), i, uri, value)


def PaaS(api):
    for i in api:
        for value in api[i].values():
            if i == 'geolocation':
                uri = '/geolocation/v1/' + value
            elif i == 'mailer':
                uri = '/api/v1/' + value
            else:
                continue
            resCheck(auth_Hmac(uri), i, uri, value)


def App(api):
    for i in api:
        for value in api[i].values():
            url = value
            uri = url[url.find('apigw.ntruss.com')+len('apigw.ntruss.com'):]

            if i == 'apigateway' :
                resCheck(auth_Hmac(uri), i, uri, i)
            else:
                # resCheck(rescode, i, uri, data='')
                req = auth_v1(url)
                if i == 'searchtrend':
                    data = "{\"startDate\":\"2017-01-01\",\"endDate\":\"2017-04-30\",\"timeUnit\":\"month\",\"keywordGroups\":[{\"groupName\":\"한글\",\"keywords\":[\"한글\",\"korean\"]},{\"groupName\":\"영어\",\"keywords\":[\"영어\",\"english\"]}],\"device\":\"pc\",\"ages\":[\"1\",\"2\"],\"gender\":\"f\"}";
                elif i == 'clova':
                    data = "speaker=mijin&speed=0&text=" + urllib.parse.quote("안녕하세요.")
                elif i == 'nshorturl':
                    data = "url=" + urllib.parse.quote("http://d2.naver.com/helloworld/4874130")
                elif i == 'papago':
                    papagoDict()
                    pArr = papagoDict.SmtArr
                    if value == "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation":
                        pArr = papagoDict.NmtArr

                    for s, t in pArr.items():
                        for p in range(len(t)):
                            data = 'source=' + s + '&target=' + t[p] + '&text=' + papagoDict.LangText[s]
                            if list(pArr.keys())[-1] == s:
                                break
                            name=nameCheck(uri)
                            resCheck(req, i, uri, name+'-'+s+'-'+t[p], data)
                else:
                    data = ''
                resCheck(req, i, uri, i+uri, data)


if __name__ == '__main__':
    sys.path.append('/apps/web_root/Python')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learning_log.settings')
    import django
    django.setup()
    from ncloud.models import NaverApiErrorLog, NaverApiStatus
    global count
    count = 1
    print('\n--------------------------------------')
    print(datetime.datetime.now())
    print('\nIaaS')
    IaaS(IaaS_API(0))
    print('\nPaaS')
    PaaS(PaaS_API(0))
    print('\nAi Application')
    App(App_API(0))
    print(datetime.datetime.now())

    # test = {'rescode': 'rescode', 'uri': 'uri', 'name': 'mail test'}
    # Mail(test)

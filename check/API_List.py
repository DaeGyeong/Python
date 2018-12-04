from django.http import HttpResponse
import json, urllib.request, datetime



def IaaS_API(request):
    instanceNum = ''
    time = timearr()
    uri = {
        'server' : {
            # getServerImageProductList ( 서버이미지 상품 리스트 조회 )
            "1" : 'getServerImageProductList',
            # getServerProductList ( 서버 상품 리스트 조회 ) + serverImageProductCode 쿼리 필수
            "2" : 'getServerProductList' + '?serverImageProductCode=SPSW0LINUX000031',
            # getRaidList ( RAID 리스트 조회 )
            "3" : 'getRaidList',
            # getZoneList ( ZONE 리스트 조회 )
            "4" : 'getZoneList',
            # getRegionList ( REGION 리스트 조회)
            "5" : 'getRegionList',
            # getNasVolumeInstanceList ( NAS 볼륨 인스턴스 리스트 조회 )
            "6" : 'getNasVolumeInstanceList',
            # getAccessControlGroupList( 접근제어 그룹 리스트 조회)
            "7" : 'getAccessControlGroupList',
            # getAccessControlGroupServerInstanceList ( 접근제어 그룹 적용된 서버 인스턴스 리스트 조회 ) + accessControlGroupConfigurationNo 쿼리 필수
            "8" : 'getAccessControlGroupServerInstanceList' + "?accessControlGroupConfigurationNo=" + instanceNum,
            # getAccessControlRuleList ( 접근제어 규칙 리스트 조회 ) + accessControlGroupConfigurationNo 쿼리 필수
            "9" : 'getAccessControlRuleList' + '?accessControlGroupConfigurationNo=' + instanceNum,
            # getServerInstanceList ( 서버 인스턴스 리스트 조회 )
            "10" : 'getServerInstanceList',
            # getMemberServerImageList ( 회원 서버 이미지 리스트 조회 )
            "11" : 'getMemberServerImageList',
            # getBlockStorageInstanceList ( 블록 스토리지 인스턴스 리스트 조회 )
            "12" : 'getBlockStorageInstanceList',
            # getBlockStorageSnapshotInstanceList ( 블록 스토리지 스냅샷 인스턴스 리스트 조회 )
            "13" : 'getBlockStorageSnapshotInstanceList',
            # getPublicIpInstanceList ( 공인 IP 인스턴스 리스트 조회 )
            "14" : 'getPublicIpInstanceList',
            # getPortForwardingRuleList ( 포트 포워딩 Rule 리스트 조회)
            "15" : 'getPortForwardingRuleList'
        },
        'lb' : {
            # LB 인스턴스 리스트
            '1' : 'getLoadBalancerInstanceList',
            # LB SSL 인증서조회
            '2' : 'getLoadBalancerSslCertificateList'
        },
        'autoscaling' : {
            # 론치설정 리스트
            '1' : 'getLaunchConfigurationList',
            # 그룹 리스트
            '2' : 'getAutoScalingGroupList',
            # 스케쥴액션 리스트
            '3' : 'getScheduledActionList',
            # 프로세스 구분 리스트
            '4' : 'getScalingProcessTypeList',
            # 액티비티 로그 리스트
            '5' : 'getAutoScalingActivityLogList',
            # 오토스케일링 설정 로그 리스트
            '6' : 'getAutoScalingConfigurationLogList',
            # 오토스케일링 정책 리스트
            '7' : 'getAutoScalingPolicyList',
            # 조정유형 리스트
            '8' : 'getAdjustmentTypeList'
        },
        'monitoring' : {
            # Metric별 통계 정보 조회
            '1' : 'getMetricStatistics?' + 'instanceNoList.1=' + instanceNum + '&metricName=CPUUtilization&startTime='+ time[0] +'&endTime='+ time[1] +'&period=1800',
            # Metric 리스트 조회
            '2' : 'getListMetrics?' + 'instanceNo=' + instanceNum
        },
        'security' : {
            # '1' : 'getAppInstanceStatistics' + '?appInstanceNo='
        },
        'cdn' : {
            # CDN+ 인스턴스리스트
            '1' : 'getCdnPlusInstanceList',
            # Global CDN 인스턴스리스트
            '2' : 'getGlobalCdnInstanceList'
        },
        'clouddb' : {
            # CloudDB Config group 조회
            '1' : 'getCloudDBConfigGroupList?dbKindCode=MYSQL',
            # CloudDB 상품 리스트
            '2' : 'getCloudDBImageProductList?dbKindCode=MYSQL',
            # CloudDB 이미지 상품 리스트
            # '3' : 'getCloudDBProductListRequest' + '?'
        }
    }
    if request==0:
        return uri
    else:
        return HttpResponse(json.dumps(uri), content_type='application/json')

def PaaS_API(request):
    uri = {
    # /geolocation/v1/
        'geolocation' : {
            '1' : 'geoLocation?ip=202.131.30.11'
        },
        'mailer': {
            '1' : 'mails/requests/20181022000000073804/status'
        }
    }
    if request==0:
        return uri
    else:
        return HttpResponse(json.dumps(uri), content_type='application/json')

def App_API(request):
    uri = {
        'clova' : {
            '1' : 'https://naveropenapi.apigw.ntruss.com/voice/v1/tts'
        },
        'maps' : {
            '1' : 'https://naveropenapi.apigw.ntruss.com/map/v1/geocode?query=%EB%B6%88%EC%A0%95%EB%A1%9C%206'
        },
        'papago' : {
            '1' : 'https://naveropenapi.apigw.ntruss.com/smt/v1/translation',
            '2' : 'https://naveropenapi.apigw.ntruss.com/nmt/v1/translation'
        },
        'nshorturl' : {
            '1' : 'https://naveropenapi.apigw.ntruss.com/util/v1/shorturl',
            #'2' : 'https://naveropenapi.apigw.ntruss.com/util/v1/shorturl?url=http://d2.naver.com/helloworld/4874130'
        },
        'captcha' : {
            '1' : 'https://naveropenapi.apigw.ntruss.com/captcha/v1/nkey?code=0',
            '2' : 'https://naveropenapi.apigw.ntruss.com/scaptcha/v1/skey?code=0'
        },
        'searchtrend' : {
            '1' : 'https://naveropenapi.apigw.ntruss.com/datalab/v1/search'
        },
        'apigateway' : {
            '1' : 'https://ta50do4nv5.apigw.ntruss.com/api-test/v1/api'
        }
    }
    if request == 0:
        return uri
    else:
        return HttpResponse(json.dumps(uri), content_type='application/json')


def timearr():
    ntime = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")
    ntime = list(ntime)
    hh = int(datetime.datetime.today().strftime("%H"))
    btime = list(ntime)
    if hh == 0:
        nh = '00'
        bh = '23'
        bd = int(datetime.datetime.today().strftime("%d")) - 1
        if bd == 0 :
            month = int(datetime.datetime.today().strftime("%m")) - 1
            if month==4 or month==6 or month==9 or month==11:
                bd = '30'
            elif month == 2:
                year = int(datetime.datetime.today().strftime("%Y"))
                if (year%4==0 and y%100 !=0) or year % 400 == 0:
                    bd = '29'
                else :
                    bd = '28'
            else:
                bd = '31'
            btime[5:7] = repr(month)
        elif bd < 10:
            bd = '0' + repr(bd)
        else:
            bd = repr(bd)
        btime[8:10] = bd

    elif hh < 10:
        nh = '0' + repr(hh)
        bh = '0' + repr(int(hh) - 1)

    else:
        nh = repr(hh)
        if int(hh) <= 10:
            bh = '0' + repr(int(hh) - 1)
        else:
            bh = repr(int(hh) - 1)

    ntime[11:13] = nh
    ntime = ''.join(ntime)
    btime[11:13] = bh
    btime = ''.join(btime)

    return [btime, ntime]


def papagoDict():
    papagoDict.LangText = {
        'ko' : '안녕하세요',
        'ja' : 'お会いできて嬉しいです',
        'en' : 'Nice to meet you',
        'zh-CN' : '很高兴见到你',
        'zh-TW' : '很高興見到你',
        'es' : 'Encantado de conocerle',
        'fr' : 'Je suis content de vous rencontrer',
        'vi' : 'Rất vui được gặp các bạn',
        'th' : 'ยินดีที่ได้พบคุณ',
        'id' : 'Senang bertemu dengan Anda',
    }
    papagoDict.SmtArr = {
        'ko' : ['en','ja', 'zh-CN'],
        'en' : ['ko'],
        'ja' : ['ko'],
        'zh-CN' : ['ko'],
    }
    papagoDict.NmtArr = {
        # ko<->en, ko <-> zh-CN, ko <-> zh-TW, ko<->es, ko<->fr, ko<->vi, ko<->th, ko<->id, en<->ja, en<->fr 조합만 가능
        'ko' : ['en', 'zh-CN', 'zh-TW', 'es', 'fr', 'vi', 'th', 'id'],
        'en' : ['ko', 'ja', 'fr'],
        'zh-CN' : ['ko'],
        'zh-TW' : ['ko'],
        'es' : ['ko'],
        'fr' : ['ko', 'en'],
        'vi' : ['ko'],
        'th' : ['ko'],
        'id' : ['ko'],
        'ja' : ['en'],
    }

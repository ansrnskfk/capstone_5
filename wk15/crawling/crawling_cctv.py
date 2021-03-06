import urllib.request
import datetime
import json

ServiceKey = "jhPdJwd22r%2BeOuAA5jWR2YuNOAajqH6TXIQOEJjHGX3%2F%2BWJs4XexNQkVkEykw3aiOlvKUKgYY%2FSe49ifSsJvVw%3D%3D"

def getRequestUrl(url):
    req = urllib.request.Request(url)   # url 접속을 요청하는 객체
    try:
        response = urllib.request.urlopen(req)  # 요청받은 req에 대한 공공데이터 서버의 응답을 response에 저장
        if response.getcode() == 200:   # getcode()로 response 객체에 저장된 코드를 확인. 200인지 아닌지 확인. getcode()는 요청 처리에 대한 응답 상태를 확인하는 함수. 200이면 성공
            print("[%s] Url Request Success" % datetime.datetime.now()) #200이면 정상처리 된 것이므로 현재 시간과 함께 성공 메시지를 출력
            return response.read().decode('utf-8')  # 응답을 utf-8 형식으로 디코딩하여 반환
    except Exception as e:  # 예외사항 발생시 해당 에러 메시지(e) 출력
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))   # 현재 시간과 에러가 발생한 url 출력
        return None


# url 작성 후 line 11 함수 호출하고 응답받은 데이터를 json형태로 저장하는 함수
def getCctv():
    service_url = "https://api.odcloud.kr/api/15084631/v1/uddi:6835621c-b29c-4972-b0f2-8010d2dae40b?page=1&perPage=4817&serviceKey="
    url = service_url + ServiceKey

    responseDecode = getRequestUrl(url)

    if (responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)


# line 24 함수 호출 후 원하는 데이터 추출 하는 함수
def getInfo():
    jsonData = getCctv()    # line 24 함수 호출
    jsonResult = []
    num = 0

    for index in range(len(jsonData['data'])):
        latitude = jsonData['data'][index]['위도']
        longitude = jsonData['data'][index]['경도']
        adress = jsonData['data'][index]['소재지지번주소']
        manager_name = jsonData['data'][index]['관리기관명']
        phonenumber = jsonData['data'][index]['관리기관전화번호']



        if '동구' in adress:  # 동구에 있는 cctv만 추출
            if latitude and longitude:    # 위경도의 정보가 없는 cctv 제거
                if float(latitude) > float(longitude):  # 만약 위경도의 정보가 서로 바뀌어 있으면
                    latitude, longitude = longitude, latitude   # 다시 원상태로
                jsonResult.append(  # 추출한 정보를 딕셔너리 형태로 저장
                    {'num': num, 'longitude': longitude, 'latitude': latitude, 'adress': adress, 'manager_name': manager_name,
                    'phonenumber': phonenumber})
                num += 1
    # for i in jsonResult:
    #     print(i)
    return jsonResult

getInfo()
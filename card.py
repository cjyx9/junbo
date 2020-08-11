import requests
from json import loads
from os import system

system('cls')

# !-全局变量定义-!
useraccount = '2022881415'
userpwd = 'cjy2007719'
# useraccount = input("用户名:")
# userpwd = input("密码:")
# 获取用户输入
AppCode = 'mX57mPcYRWk='
# 手机app的key
login_api = 'http://open.aedu.cn/passport/mobilelogin'
# 登录取cookie

agent = 'Mozilla/5.0 (Linux; Android 6.0.1; Redmi 4 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.149 Mobile Safari/537.36'
headers = {
    "Connection": 'keep-alive',
    "User-Agent": agent
}
# 构造 Request headers

payload_login = {
    'useraccount':useraccount,
    'userpwd':userpwd,
    'AppCode':AppCode,
    'format':'json'
}
# 传入的参数
# !-全局变量定义-!

try:
    session = requests.Session()
    # 打开会话
    login_response = session.post(url=login_api, headers=headers, data=payload_login)
    # 登录亚教网
    # print("服务器端返回状态码：", login_response.status_code)

    token_api = "http://passport.aedu.cn/api/GetCurrentUserInfo?callback=?"
    token_response = session.get(url=token_api, headers=headers)
    # 获取具体信息及token
    info_json = loads(token_response.text[2:-1])
    # json数据
    # print(info_json)

    # !-全局变量定义-!
    token = info_json['Token']
    name = info_json['UserName']
    school_name = info_json['SchoolName']
    user_id = info_json['Id']
    school_id = info_json['SchoolId']
    class_id = info_json['ClassId']
    face_img = info_json['UserFace']
    headers['UserLoginToken'] = token
    headers['Authorization'] = "Basic " + token
    # !-全局变量定义-!

    print('你好啊~%s!以下是班级成员名单:'%(name))
    # members_api = "http://mobileapi.aedu.cn/users/desk-linkMan-group"
    # 这个api获取出的竟然是全校教职工名单😂
    members_api = "http://mobileapi.aedu.cn/users/group-users?groupId=S" + str(class_id)
    members_response = session.get(url=members_api, headers=headers)
    members_json = loads(members_response.text)
    # members = members_json['data']['systemSettedGroups'][0]['systemSettedGroupMembers']
    members = members_json['data']
    for person in members:
        if person['userRole']==3:
            print(person['userName'], '教师', person['subjectName'])
        elif person['userRole']==4:
            print(person['userName'], '班主任', person['subjectName'])
        elif person['userRole']==1:
            print(person['userName'], '学生')
        else:
            print(person['userName'], '未知')
    print('总人数:',len(members),school_name)

    print('现在正在获取作业信息...')
    homework_api = 'http://newapi.aedu.cn/app-api/api/v1/messages/received-list?pageIndex=1&pageSize=10&msgTypes=8&isUpdateReadStatus=true'
    # 调整pagesize参数修改显示条数
    homework_response = session.get(url=homework_api, headers=headers)
    homework_json = loads(homework_response.text)
    homeworks = homework_json['data']
    markdown_text = '## 亚教网作业\n'
    for item in homeworks:
        line = '- ' + item['text'].replace('家长您好，亚教网老师给您发了一条','').replace('，请登录到智慧云人人通app进行查看。',' ').replace('，请登录到智慧云人人通app进行查看',' ') + '**' + item['senderName'] + '**\n' + '![作业提醒](' + item['images'] + ')\n'
        markdown_text += line
    file = open('homework.md', 'w')
    file.write(markdown_text)
    print("已将作业写入到homework.md中!")
    file.close()
    # 都一个套路👀
except BaseException as log:
    system('cls')
    print('哦豁,出现错误了~请检查自己的网络及密码输入有无错误,\n如果不能解决,请将错误报告发送给开发者:', log)
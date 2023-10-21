#！/usr/bin/env python
import re
import sys
from random import randint
import time
import json
import threading
import requests
from src import getCookies


session = requests.Session()


def printline():
    print('-' * 51)


def startstudy(learntime, x):
    #    print('\n位置: '+x['location']+'\n已学习: '+x['learntime']+'
    #    即将学习'+str(learntime)+'秒～',end='')
    scoid = x['id']
    url = 'https://welearn.sflep.com/Ajax/SCO.aspx'
    req1 = session.post(
        url,
        data={
            'action': 'getscoinfo_v7',
            'uid': uid,
            'cid': cid,
            'scoid': scoid
        },
        headers={
            'Referer': 'https://welearn.sflep.com/student/StudyCourse.aspx'
        })
    if ('学习数据不正确' in req1.text):
        req1 = session.post(
            url,
            data={
                'action': 'startsco160928',
                'uid': uid,
                'cid': cid,
                'scoid': scoid
            },
            headers={
                'Referer': 'https://welearn.sflep.com/student/StudyCourse.aspx'
            })
        req1 = session.post(
            url,
            data={
                'action': 'getscoinfo_v7',
                'uid': uid,
                'cid': cid,
                'scoid': scoid
            },
            headers={
                'Referer': 'https://welearn.sflep.com/student/StudyCourse.aspx'
            })
        if ('学习数据不正确' in req1.text):
            print('\n错误:', x['location'])
            return 0
    back = json.loads(req1.text)['comment']
    if ('cmi' in back):
        back = json.loads(back)['cmi']
        cstatus = back['completion_status']
        progress = back['progress_measure']
        session_time = back['session_time']
        total_time = back['total_time']
        crate = back['score']['scaled']
    else:
        cstatus = 'not_attempted'
        progress = session_time = total_time = '0'
        crate = ''
    url = 'https://welearn.sflep.com/Ajax/SCO.aspx'
    req1 = session.post(
        url,
        data={
            'action': 'keepsco_with_getticket_with_updatecmitime',
            'uid': uid,
            'cid': cid,
            'scoid': scoid,
            'session_time': session_time,
            'total_time': total_time
        },
        headers={
            'Referer': 'https://welearn.sflep.com/student/StudyCourse.aspx'
        })
    for nowtime in range(1, learntime + 1):
        #        print(str(nowtime)+'～',end='')
        time.sleep(1)
        if (nowtime % 60 == 0):
            #            print('发送心跳包～',end='')
            url = 'https://welearn.sflep.com/Ajax/SCO.aspx'
            req1 = session.post(
                url,
                data={
                    'action': 'keepsco_with_getticket_with_updatecmitime',
                    'uid': uid,
                    'cid': cid,
                    'scoid': scoid,
                    'session_time': session_time,
                    'total_time': total_time
                },
                headers={
                    'Referer':
                    'https://welearn.sflep.com/student/StudyCourse.aspx'
                })


#    print('增加学习时间～')
    url = 'https://welearn.sflep.com/Ajax/SCO.aspx'
    req1 = session.post(
        url,
        data={
            'action': 'savescoinfo160928',
            'cid': cid,
            'scoid': scoid,
            'uid': uid,
            'progress': progress,
            'crate': crate,
            'status': 'unknown',
            'cstatus': cstatus,
            'trycount': '0'
        },
        headers={
            'Referer': 'https://welearn.sflep.com/Student/StudyCourse.aspx'
        })


class NewThread(threading.Thread):
    def __init__(self, learntime, x):
        threading.Thread.__init__(self)
        self.deamon = True
        self.learntime = learntime
        self.x = x

    def run(self):
        startstudy(self.learntime, self.x)


try:  # from command line
    cookie = getCookies.getFromCommand()
    # cookie = eval(open("./cookies.txt", 'r').read())
except:
    printline()
    try:
        # cookie = dict(
        #     map(lambda x: x.split('=', 1),
        #         open('cookies.txt', 'r').read().split(';')))
        cookie = getCookies.getCookiesFromUser()
    except:
        print('Cookie输入错误!!!')
        sys.exit(1)
for k, v in cookie.items():
    session.cookies[k] = v
printline()
while True:
    # 查询课程信息
    url = "https://welearn.sflep.com/ajax/authCourse.aspx?action=gmc"
    response = session.get(
        url,
        headers={"Referer": "https://welearn.sflep.com/student/index.aspx"})
    if '\"clist\":[]}' in response.text:
        input('发生错误!!!可能是登录错误或没有课程!!!')
        sys.exit(1)
    else:
        print('查询课程成功!!!')
        printline()
        print('我的课程: \n')
    back = response.json()["clist"]
    print('[NO. 0]  退出程序')
    for i, course in enumerate(back, start=1):
        print(f'[NO.{i:>2}] 完成度{course["per"]:>3}% {course["name"]}')

    # 选择课程
    order = int(input("\n请输入需要完成的课程序号（上方[]内的数字）: "))
    if (order == 0):
        sys.exit(0)
    cid = back[order - 1]["cid"]
    printline()
    print("获取单元中...")
    printline()
    # 刷课模块
    url = f"https://welearn.sflep.com/student/course_info.aspx?cid={cid}"
    response = session.get(url)

    uid = re.search('"uid":(.*?),', response.text).group(1)
    classid = re.search('"classid":"(.*?)"', response.text).group(1)

    url = 'https://welearn.sflep.com/ajax/StudyStat.aspx'
    response = session.get(
        url,
        params={
            'action': 'courseunits',
            'cid': cid,
            'uid': uid
        },
        headers={
            'Referer': 'https://welearn.sflep.com/student/course_info.aspx'
        })
    back = response.json()['info']

    # 选择单元 使用了WELearnToSleeep的代码
    print('[NO. 0]  按顺序完成全部单元课程')
    unitsnum = len(back)
    for i, x in enumerate(back, start=1):
        if x['visible'] == 'true':
            print(f'[NO.{i:>2d}]  [已开放]  {x["unitname"]}  {x["name"]}')
        else:
            print(f'[NO.{i:>2d}] ![未开放]! {x["unitname"]}  {x["name"]}')
    unitidx = int(input('\n\n请选择需要完成的单元序号（上方[]内的数字，输入0为按顺序刷全部单元）： '))
    printline()
    inputcrate = input(
        '模式1:每个练习指定正确率，请直接输入指定的正确率\n如:希望每个练习正确率均为100，则输入 100\n\n模式2:每个练习随机正确率，请输入正确率上下限并用英文逗号隔开\n如:希望每个练习正确率为70～100，则输入 70,100\n\n请严格按照以上格式输入每个练习的正确率: '
    )
    if ',' in inputcrate:
        mycrate = eval(inputcrate)
        randommode = True
    else:
        mycrate = inputcrate
        randommode = False
    printline()
    inputdata = input(
        '\n\n\n模式1:每个练习增加指定学习时长，请直接输入时间\n如:希望每个练习增加30秒，则输入 30\n\n模式2:每个练习增加随机时长，请输入时间上下限并用英文逗号隔开\n如:希望每个练习增加10～30秒，则输入 10,30\n\n\n请严格按照以上格式输入: '
    )
    if (',' in inputdata):
        inputtime = eval(inputdata)
        mode = 2
    else:
        inputtime = int(inputdata)
        mode = 1
    printline()
    # 伪造请求
    way1Succeed, way2Succeed, way1Failed, way2Failed = 0, 0, 0, 0

    ajaxUrl = "https://welearn.sflep.com/Ajax/SCO.aspx"
    infoHeaders = {
        "Referer":
        f"https://welearn.sflep.com/student/course_info.aspx?cid={cid}",
    }

    if (unitidx == 0):
        i = 0
    else:
        i = unitidx - 1
        unitsnum = unitidx

    while True:
        response = session.get(
            f'https://welearn.sflep.com/ajax/StudyStat.aspx?action=scoLeaves&cid={cid}&uid={uid}&unitidx={i}&classid={classid}',
            headers=infoHeaders)

        if "异常" in response.text or "出错了" in response.text:
            break

        for course in response.json()["info"]:
            if course['isvisible'] == 'false':  # 跳过未开放课程
                print(f'[!!跳过!!]    {course["location"]}')
            elif "未" in course["iscomplete"]:  # 章节未完成
                print(f'[即将完成]    {course["location"]}')
                if randommode is True:
                    crate = str(randint(mycrate[0], mycrate[1]))
                else:
                    crate = mycrate
                data = '{"cmi":{"completion_status":"completed","interactions":[],"launch_data":"","progress_measure":"1","score":{"scaled":"' + crate + \
                    '","raw":"100"},"session_time":"0","success_status":"unknown","total_time":"0","mode":"normal"},"adl":{"data":[]},"cci":{"data":[],"service":{"dictionary":{"headword":"","short_cuts":""},"new_words":[],"notes":[],"writing_marking":[],"record":{"files":[]},"play":{"offline_media_id":"9999"}},"retry_count":"0","submit_time":""}}[INTERACTIONINFO]'

                id = course["id"]
                session.post(
                    ajaxUrl,
                    data={
                        "action": "startsco160928",
                        "cid": cid,
                        "scoid": id,
                        "uid": uid
                    },
                    headers={
                        "Referer":
                        f"https://welearn.sflep.com/Student/StudyCourse.aspx?cid={cid}&classid={classid}&sco={id}"
                    })
                response = session.post(
                    ajaxUrl,
                    data={
                        "action": "setscoinfo",
                        "cid": cid,
                        "scoid": id,
                        "uid": uid,
                        "data": data,
                        "isend": "False"
                    },
                    headers={
                        "Referer":
                        f"https://welearn.sflep.com/Student/StudyCourse.aspx?cid={cid}&classid={classid}&sco={id}"
                    })
                print(f'>>>>>>>>>>>>>>正确率:{crate:>3}%', end='  ')
                if '"ret":0' in response.text:
                    print("方式1:成功!!!", end="  ")
                    way1Succeed += 1
                else:
                    print("方式1:失败!!!", end="  ")
                    way1Failed += 1

                response = session.post(
                    ajaxUrl,
                    data={
                        "action": "savescoinfo160928",
                        "cid": cid,
                        "scoid": id,
                        "uid": uid,
                        "progress": "100",
                        "crate": crate,
                        "status": "unknown",
                        "cstatus": "completed",
                        "trycount": "0",
                    },
                    headers={
                        "Referer":
                        f"https://welearn.sflep.com/Student/StudyCourse.aspx?cid={cid}&classid={classid}&sco={id}"
                    })
                #                sleep(1) # 延迟1秒防止服务器压力过大
                if '"ret":0' in response.text:
                    print("方式2:成功!!!")
                    way2Succeed += 1
                else:
                    print("方式2:失败!!!")
                    way2Failed += 1
            else:  # 章节已完成
                print(f'[ 已完成 ]    {course["location"]}')

        if unitidx != 0:
            break
        else:
            i += 1

    url = 'https://welearn.sflep.com/ajax/authCourse.aspx?action=gmc'
    req = session.get(
        url,
        headers={'Referer': 'https://welearn.sflep.com/student/index.aspx'})
    back = json.loads(req.text)['clist']
    cid = str(back[order - 1]['cid'])
    url = 'https://welearn.sflep.com/student/course_info.aspx?cid=' + cid
    req = session.get(
        url,
        headers={'Referer': 'https://welearn.sflep.com/student/index.aspx'})
    uid = req.text[req.text.find('"uid":') +
                   6:req.text.find('"',
                                   req.text.find('"uid":') + 7) - 2]
    classid = req.text[req.text.find('classid=') +
                       8:req.text.find('&',
                                       req.text.find('classid=') + 9)]

    url = 'https://welearn.sflep.com/ajax/StudyStat.aspx'
    req = session.get(url,
                      params={
                          'action': 'courseunits',
                          'cid': cid,
                          'uid': uid
                      },
                      headers={
                          'Referer':
                          'https://welearn.sflep.com/student/course_info.aspx'
                      })
    back = json.loads(req.text)['info']
    threads = 100  # 最大线程数设置
    running = []
    runningnumber = maxtime = 0
    wrong = []

    if (unitidx == 0):
        i = 0
    else:
        i = unitidx - 1
        unitsnum = unitidx

#    while '异常' not in req.text and '出错了' not in req.text:
    for unit in range(i, unitsnum):
        url = 'https://welearn.sflep.com/ajax/StudyStat.aspx?action=scoLeaves&cid=' + cid + '&uid=' + uid + '&unitidx=' + str(
            unit) + '&classid=' + classid
        req = session.get(
            url,
            headers={
                'Referer':
                'https://welearn.sflep.com/student/course_info.aspx?cid=' + cid
            })
        back = json.loads(req.text)['info']
        for x in back:
            if (mode == 1):
                learntime = inputtime
            else:
                learntime = randint(inputtime[0], inputtime[1])
            if (runningnumber == threads):
                for nowtime in range(1, maxtime + 1):
                    print('\r已启动线程:',
                          runningnumber,
                          '当前秒数:',
                          nowtime,
                          '秒，总时间:',
                          maxtime,
                          '秒',
                          end='')
                    time.sleep(1)
                print('  等待线程退出…')
                for t in running:
                    t.join()
                runningnumber = maxtime = 0
                running = []
            running.append(NewThread(learntime, x))
            running[runningnumber].start()
            runningnumber += 1
            if (learntime > maxtime):
                maxtime = learntime
            print('线程:', runningnumber, '位置:', x['location'], '\n已学: ',
                  x['learntime'], '将学:', learntime, '秒')

        if (runningnumber > 0):
            for nowtime in range(1, maxtime + 1):
                print('\r已启动线程:',
                      runningnumber,
                      '当前秒数:',
                      nowtime,
                      '秒，总时间:',
                      maxtime,
                      '秒',
                      end='')
                time.sleep(1)
            print('  等待线程退出…')
            for t in range(runningnumber):
                running[t].join()
            runningnumber = maxtime = 0
            running = []

    if unitidx == 0:
        break
    else:
        print('本单元运行完毕！回到选课处！！\n\n\n\n')
        printline()

printline()
print(f"""
***************************************************
全部完成!!

总计:
方式1: {way1Succeed} 成功, {way1Failed} 失败
方式2: {way2Succeed} 成功, {way2Failed} 失败

***************************************************""")
input("按任意键退出")

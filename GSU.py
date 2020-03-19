import requests
import json
import sys
import re

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"

def OpenHosts():
    with open('hosts.json', 'r+') as f:
        return json.loads(f.read())


def WriteHosts(data):
    try:
        with open('hosts.json', 'w+') as f:
            f.write(data)
    except:
        print('error')


def GetLocalIP():
    try:
        Server = 'https://www.ip.cn/'
        IP = requests.get(Server, headers=headers)
        front = len('<p>您现在的 IP：<code>')
        end = len('</code></p><p>')*(-1)
        return re.search('<p>您现在的 IP：<code>.*?</code></p><p>', IP.text)[0][front:end]
    except:
        return ''

def DNS(domain):
    Server = 'http://119.29.29.29/d?dn='
    Locals = '&ip=' + LocalIP
    back = requests.get(Server + domain + Locals,headers=headers)
    passage = ''
    IP = []
    for i in back.text:
        if i == ';':
            IP.append(passage)
            passage = ''
            continue
        passage += i
    IP.append(passage)
    return IP


def WebDNS(data):
    domain_ip = []
    for i in data:
        domans = data[i]
        domain_ip.append(DNS(domans)[0] + ' ' + domans)
    return domain_ip


def helps():
    print('python GSU.py [command]')
    print('[command]: ')
    print('     help         (help you find help document)')
    print('     add [domain] (add domain for check)')
    print('      └┈┈ add -y  (pass the confirm part)')
    print('     ls           (print the list of domain )')
    print('     rm [id]      (del the domain from the list)')
    print('      └┈┈ rm -y   (pass the confirm part)')
    print('     do           (print the hosts)')
    print('     save [file]  (save hosts to a file)')


if __name__ == "__main__":
    global LocalIP
    LocalIP = GetLocalIP()

    try:
        data = OpenHosts()
    except:
        data = {}
        print('Base data is broken')
    argv = sys.argv
    try:
        if(argv[1] == 'help'):
            helps()
        # help
        elif argv[1] == 'add':
            try:
                argvID = 2
                confirm = 'n'
                if argv[2] == '-y':
                    argvID += 1
                    confirm = 'y'
                else:
                    print('Your domain:', argv[2])
                    confirm = input('Make sure you want to add this domain (y/n)')
                    
                lens = len(data)
                # len获取元素数量，正好比字典下标多1
                if str(confirm) == 'y':
                    data.update({lens: argv[argvID]})
                WriteHosts(json.dumps(data))
            except:
                helps()
                print('please check')
        # add
        elif argv[1] == 'ls':
            print('ID', 'Domain')
            for i in data:
                print(i, data[i])
        # ls
        elif argv[1] == 'rm':
            argvID = 2
            confirm = 'n'
            if argv[2] == '-y':
                argvID += 1
                confirm = 'y'
            else:
                print('Your choose:', argv[2])
                confirm = input('Make sure you want to remove this domain (y/n)')
            lens = len(data)
            if str(confirm) == 'y':
                for i in range(int(argv[argvID]), lens-1):
                    data[str(i)] = data[str(i+1)]
                data.pop(str(lens-1))
                WriteHosts(json.dumps(data))
        # rm
        elif argv[1] == 'do':
            print('=============================================')
            for i in WebDNS(data):
                print(i)
            print('=============================================')
        elif argv[1] == 'save':
            Text = ''
            argv[1]
            for i in WebDNS(data):
                Text += i +'\n'
            try:
                with open(argv[2],'w+') as f:
                    f.write(Text)
                print('Successful')
            except:
                print('error')
        # do
        else:
            helps()
            print('Please make sure you enter the true command line')
    except:
        helps()
        print('Please make sure you enter the true command line')
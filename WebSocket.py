# _*_ coding:utf-8 _*_
# FileName: WebSocket.py
# IDE: PyCharm

import json
import time
import asyncio
import paramiko
import websockets
from socket import timeout
from websockets.exceptions import ConnectionClosedError

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)


def run_cmd(command):
    if command[:2] == 'll':
        command = 'ls' + (command[2:].replace('-', '-l') if '-' in command[2:] else ' -l')
    if command in ['sh', 'bash']:
        return '不支持在WebShell中启用新的终端！（请不要在WebShell中套娃！）'
    s_in, s_out, s_err = client.exec_command(command)
    # print('\033[0;32mIn: \033[0m' + (s_in.read().decode('utf-8').strip('\n') if s_in.readable() else ''))
    # print('\033[0;32mOut: \033[0m' + (s_out.read().decode('utf-8').strip('\n') if s_out.readable() else ''))
    # print('\033[0;32mErr: \033[0m' + (s_err.read().decode('utf-8').strip('\n') if s_err.readable() else ''))
    while s_out.readable():
        res = s_out.readline()
        if not res:
            break
        yield res
    while s_err.readable():
        res = s_err.readline()
        if not res:
            break
        yield res
    yield ''
    # return s_out.readable() and s_out.read().decode('utf-8').strip('\n') or s_err.readable() and s_err.read().decode('utf-8').strip('\n') or ''


async def handle(websocket, path):
    print('已连接到WebSocket')
    try:
        text = ''
        user = ''
        overtime = 22
        async for message in websocket:
            try:
                if len(message) > 2:
                    if path == '/shell':
                        message = json.loads(message)
                        try:
                            if not user and message['operate'] == 'connect':
                                if not user:
                                    client.connect(hostname=message['host'],
                                                   port=int(message['port']),
                                                   username=message['username'],
                                                   password=message['password'],
                                                   timeout=3)
                                    overtime = message['time']
                                    user = '#' if message['username'] == 'root' else '$'
                                res = f'\n\r{user} '
                            else:
                                res = f'当前操作 “ {message["operate"]} ” 未被定义，消息 ” {message} “ 处理失败！'
                        except timeout:
                            res = 'IP地址、端口号可能有误，重试？'
                        except paramiko.ssh_exception.NoValidConnectionsError:
                            res = 'IP地址、端口号可能有误，重试？'
                        except paramiko.ssh_exception.AuthenticationException:
                            res = '用户名、密码可能有误，重试？'
                        except paramiko.ssh_exception.SSHException:
                            res = 'IP地址、端口号可能有误，重试？'
                        except UnicodeError:
                            res = '服务器响应错误，请刷新重试！'
                        await websocket.send(res)
                    else:
                        await websocket.send(f'当前路由 “ {path} ” 未被定义，消息 ” {message} “ 处理失败！')
                else:
                    raise json.decoder.JSONDecodeError('len(message) > 2 but not json', 'async for message in websocket:', 0)
            except json.decoder.JSONDecodeError:
                if message == '\r':
                    if text == 'exit':
                        client.close()
                        print('已和WebSocket断开连接')
                        return
                    elif text:
                        print(text)
                        await websocket.send('\n\r')
                        start = time.time()
                        for res in run_cmd(text):
                            if time.time() - start > overtime:
                                await websocket.send('Automatic timeout based on user settings.\n\r')
                                break
                            else:
                                await websocket.send(res.replace('\n', '\n\r'))
                        await websocket.send(f'{user} ')
                    text = ''
                elif message.isprintable():
                    if len(message) > 1:
                        text = message
                    else:
                        text += message
                elif message == '\b':
                    text = text[:-1]
    except ConnectionClosedError:
        print('链接已被关闭！')
        client.close()


async def main():
    async with websockets.serve(handle, "0.0.0.0", 2345):
        await asyncio.Future()


print('程序已启动！')
asyncio.run(main())

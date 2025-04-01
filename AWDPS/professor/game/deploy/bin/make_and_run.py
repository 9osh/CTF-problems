#!/usr/bin/env python3
# encoding=utf-8
import re
from pwn import *
import traceback
import mar_lib
from mar_lib import dprint,set_debug_tag,set_encrypted_flag, set_check_vul_list, set_debug_vuln, set_fsanitize_list, recvuntil_and_check,sendlineafter_and_check,recvmax_and_check,recvn_and_check,STATUS_DOWN, STATUS_ERROR, STATUS_SUCCESS

debug=False # 控制是否开启dprint及异常堆栈信息，默认关闭
is_cpp_src = False # 试题程序编程语言，默认c语言
gcc_other = "" # gcc/g++ 特殊编译选项，默认为空
question_name = "game" # 填写试题名称，用于日志记录，必须修改

# 设定需要调试的漏洞点编号0-5，标志哪些漏洞点开启context_debug，0为service_check
# 默认null为全部开启，可检测单个漏洞，如debug_vuln = [1]
debug_vuln = []
# 控制是否开启pwntools交互信息，默认关闭
context_debug=False
if debug_vuln:
    context_debug=True
# 设定漏洞编号1-5是否开启gcc的fsanitize编译选项用于辅助检测
fsanitize_list = []

# --------------------------------flag config-------------------------------------------------------------------
encrypted_flag = ['d168e9ae6ce41932ee171e4b1ada2d190aa31df90f6f9e3b1585bff3706bc0adf2d341245967fd0d1e2cf9ad5c9bb2533b17080a1ab69ad07972f96092f3d6d9024e853a1c2a06a220616c4f', 'd466eaff6be71932e81318431ada2e4c0ea91ef80f659a31168dbda1736bc5a0f2d0442c5861fc0b1b2dfbf8589eb3053c1e095118b09ad47f77fb6392a1d7dc011e82671f2b02a221636a42', 'd061e8f46ee61933e9131e431ada2c4c0bf118fc0f669e3a1188bda9716fc0a7f0d545245f37fe091f7af9a05ac8b1523b180f5c1bb798d17977fb3092a4d7d2011e866d1c2305a622626c48', 'd462edfa6de6183ced121d1919df2d4d0ea11efd0f339f6c178cbfa6766dc7adf083427e5f32fb0a1c2cfaab58c8b3573a1b0a0c1db799d47f77f93790a2d588031b86691d2a07f7216e6a4d', 'd162eaf96eeb1c3aec461f4d18d82e430ff519f808609e3d1485bef0713fc6a2f1d742245e69fb0e1f7af9ac5995b3013a1a080b1abf99d57972f86090a1d2da054c826b1e2b02a621646d1d']

# 根据debug_vuln的设定，决定是否运行check_vul函数
# 开发过程中可设定debug_vuln=[vul_id]即可单独调试该漏洞，其他漏洞默认为STATUS_DOWN状态
# debug_vuln=[] 为null代表所有漏洞开发完毕，开放所有漏洞检测
def is_debug_open(idx):
    def is_debug(func):
        def run(*args, **kwargs)->map:
            if idx in debug_vuln or not debug_vuln:
                return func(*args, **kwargs)
            elif idx == 0:
                return {"status": STATUS_SUCCESS, "msg": "service check success!"}
            return {"status": STATUS_DOWN, "msg": "vul not fix"}
        return run
    return is_debug

# arg1:v 数据列表
# arg2:log_level 日志等级
# debug开关:
#        debug==True: 输出数据
#        debug==False: 记录日志
'''
def dprint(*v, log_level=None):
'''

'''
def recvuntil_and_check(sh:process, delims):
def sendlineafter_and_check(sh:process, delims, content, drop_enter=False):
def recvmax_and_check(sh:process, length):
def recvn_and_check(sh:process, length):
'''

# check service : prev check
@is_debug_open(0)
def check_service(sh: process) -> map:
    try:
        sendlineafter_and_check(sh,b'You choice : ',b'S')
        sendlineafter_and_check(sh,b'[*] What is your name?\n',b'check_server')
        sendlineafter_and_check(sh,b'Your operation : ',b's')
        sendlineafter_and_check(sh,b'Your operation : ',b'd')
        sendlineafter_and_check(sh,b'Your operation : ',b'a')
        sendlineafter_and_check(sh,b'Your operation : ',b'w')
        sendlineafter_and_check(sh,b'Your operation : ',b'w')
        sendlineafter_and_check(sh,b'Your operation : ',b'd')
        sendlineafter_and_check(sh,b'Your operation : ',b'b')
        mark = b"  W   0w0                                                     W              W    W                        W  \n"
        msg = recvuntil_and_check(sh, mark)
        if mark not in msg:
            raise ValueError;
        sendlineafter_and_check(sh,b'Your operation : ',b'C')
        sendlineafter_and_check(sh,b"Your style of skin : ",b' aaa ')
        mark = b' aaa '
        msg = recvuntil_and_check(sh, mark)
        if mark not in msg:
            raise ValueError;
        sendlineafter_and_check(sh,b'Your operation : ',b'q')
        mark = b"You choice : "
        msg = recvuntil_and_check(sh, mark)
        if mark not in msg:
            raise ValueError;
    except:
        return {"status": STATUS_ERROR, "msg": "service check error!"}
    dprint('check_service success')
    return {"status": STATUS_SUCCESS, "msg": "check_service success"}

# buffer overflow
@is_debug_open(1)
def check_vul1(sh: process) -> map:
    try:
        sendlineafter_and_check(sh,b'You choice : ',b'S')
        sendlineafter_and_check(sh,b'[*] What is your name?\n',b'a' * 0x100)
        msg = recvuntil_and_check(sh, b'Your operation : ')
        #dprint(msg)
        if b'Your operation : ' in msg :
            dprint("vuln1 fixed")
            return {"status": STATUS_SUCCESS, "msg": "vuln1 fixed"}
        else:
            raise ValueError;
    except:
        return {"status": STATUS_DOWN, "msg": "vul1 not fix"}
# fmt
@is_debug_open(2)
def check_vul2(sh:process) -> map:
    try:
        sendlineafter_and_check(sh,b'You choice : ',b'S')
        sendlineafter_and_check(sh,b'[*] What is your name?\n',b'check_vuln2')
        sendlineafter_and_check(sh,b'Your operation : ',b'C')
        payload = b'%9$p'
        sendlineafter_and_check(sh,b"Your style of skin : ",payload)
        msg = recvuntil_and_check(sh, payload)
        if payload not in msg:
            raise ValueError
        #dprint(msg)
        dprint("vuln2 fixed")
        return {"status": STATUS_SUCCESS, "msg": "vuln2 fixed"}
    except:
        return {"status": STATUS_DOWN, "msg": "vul2 not fix"}
# off by null
@is_debug_open(3)
def check_vul3(sh) -> map:
    try:
        sendlineafter_and_check(sh,b'You choice : ',b'S')
        sendlineafter_and_check(sh,b'[*] What is your name?\n',b'check_vuln3')
        sendlineafter_and_check(sh,b'Your operation : ',b'C')
        payload = b'a' * 25
        sendlineafter_and_check(sh,b"Your style of skin : ",payload)
        for _ in range(6):
            msg = recvuntil_and_check(sh, b'\n')
        #dprint("recv msg :", msg)
        if b'a'*24 in msg and payload not in msg:
            raise ValueError
        sendlineafter_and_check(sh,b'Your operation : ',b'q')

        # can reboot game agin
        sendlineafter_and_check(sh,b'You choice : ',b'S')
        dprint("vuln3 fixed")
        return {"status": STATUS_SUCCESS, "msg": "vuln3 fixed"}
    except:
        return {"status": STATUS_DOWN, "msg": "vuln3 not fix"}

# divede 0
@is_debug_open(4)
def check_vul4(sh) -> map:
    try:
        sendlineafter_and_check(sh,b'You choice : ',b'S')
        sendlineafter_and_check(sh,b'[*] What is your name?\n',b'check_vuln4')
        for _ in range(15):
            sendlineafter_and_check(sh,b'Your operation : ',b's')
        dprint("vuln4 fixed")
        return {"status": STATUS_SUCCESS, "msg": "vuln4 fixed"}
    except:
        return {"status": STATUS_DOWN, "msg": "vuln4 not fix"}

# invalid index
@is_debug_open(5)
def check_vul5(sh) -> map:
    try:
        sendlineafter_and_check(sh,b'You choice : ',b'S')
        sendlineafter_and_check(sh,b'[*] What is your name?\n',b'check_vuln5')
        sendlineafter_and_check(sh,b'Your operation : ',b'a')
        sendlineafter_and_check(sh,b'Your operation : ',b'b')
        sendlineafter_and_check(sh,b'Your operation : ',b'a')
        sendlineafter_and_check(sh,b'Your operation : ',b'b')
        sendlineafter_and_check(sh,b'Your operation : ',b'a')
        for _ in range(5):
            sendlineafter_and_check(sh,b'Your operation : ',b'w')
        dprint("vuln5 fixed")
        return {"status": STATUS_SUCCESS, "msg": "vuln5 fixed"}
    except:
        return {"status": STATUS_DOWN, "msg": "vuln5 not fix"}

if __name__ == '__main__':
    try:
        set_debug_tag(debug,context_debug,is_cpp_src,gcc_other,question_name)
        set_encrypted_flag(encrypted_flag)
        set_check_vul_list([check_service,check_vul1,check_vul2,check_vul3,check_vul4,check_vul5])
        set_debug_vuln(debug_vuln)
        set_fsanitize_list(fsanitize_list)
        mar_lib.main()
    except Exception as e:
        if debug:
            traceback.print_exc()
        exit(1)

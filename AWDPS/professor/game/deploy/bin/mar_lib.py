#!/usr/bin/env python3
# encoding=utf-8
import re
from pwn import *
from Crypto.Cipher import ARC4
import traceback
from binascii import b2a_hex, a2b_hex
import os
import datetime
import logging
import signal

logger = logging.getLogger(__name__)
debug=False # 控制是否开启dprint及异常堆栈信息
context_debug=False # 控制是否开启pwntools交互信息
service_start_tag = b'run'
is_cpp_src = False
gcc_other = ""
target_source_path='/home/sectest/challenge/main.c'
original_source_path = "/root/main.c"
bak_source_dir = "/root/bak_main"
context.log_level = 'CRITICAL'
question_name = ""
bak_main_time = ""

# arg1:switch for debug
# arg2:switch for context_debug
# arg3:switch for is_cpp_src
# arg4:switch for gcc_other
# arg5:switch for question_name
def set_debug_tag(t_debug,t_context_debug,t_is_cpp_src,t_gcc_other,t_question_name):
    global debug,context_debug,is_cpp_src,gcc_other,target_source_path,original_source_path,question_name
    debug = t_debug
    context_debug = t_context_debug
    is_cpp_src = t_is_cpp_src
    gcc_other = t_gcc_other
    question_name = t_question_name
    # unpatched binary
    if is_cpp_src:
        target_source_path='/home/sectest/challenge/main.cpp'
        original_source_path = "/root/main.cpp"

debug_vuln = []
def set_debug_vuln(new_debug_vuln):
    global debug_vuln
    debug_vuln = new_debug_vuln

fsanitize_list = []
def set_fsanitize_list(new_fsanitize_list):
    global fsanitize_list
    fsanitize_list = new_fsanitize_list



# --------------------------------flag config-------------------------------------------------------------------
encrypted_flag = []
flag = []
flags = []

def set_encrypted_flag(flag):
    global encrypted_flag
    encrypted_flag = flag

def generate_flag():
    for i in range(5):
        flags.append(rc4_decrpt_hex(encrypted_flag[i].encode(),b'hwTeSto0'))

def generate_encflag():
    for i in range(5):
        flags.append(myRC4(flag[i].encode(),b'hwTeSto0'))
    print(flags)

def myRC4(data,key):
    rc41 = ARC4.new(key)
    encrypted = rc41.encrypt(data)
    return b2a_hex(encrypted)

def rc4_decrpt_hex(data,key):
    rc41=ARC4.new(key)
    return rc41.decrypt(a2b_hex(data))


def generate_random_str(randomlength=16):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) -1
    for i in range(randomlength):
        random_str +=base_str[random.randint(0, length)]
    return random_str.encode()
# --------------------------------flag config-------------------------------------------------------------------

# patch的行数太多
STATUE_PATCH_LINE_OUT_LIMIT_DOWN = 4
# 没编译过
STATUS_COMPILE_DOWN = 3
# 成功
STATUS_SUCCESS = 2
# 没修好 
STATUS_DOWN = 1
# 出现异常！
STATUS_ERROR=0

# 先check patch限制，再检查编译结果
PATCH_CHECK=0
COMPILE_CHECK=1
CHECK_SERVICE=2

class CustomLogger:
    def __init__(self, log_file=f'{bak_source_dir}/check.log', default_level=logging.INFO):
        # 创建日志器
        self.logger = logging.getLogger(question_name)
        self.logger.setLevel(default_level)
        
        # 创建文件处理器，并设置级别
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(default_level)
        
        # 创建控制台处理器，并设置级别
        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(default_level)
        
        # 创建日志格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        # console_handler.setFormatter(formatter)
        
        # 添加处理器到日志器
        self.logger.addHandler(file_handler)
        # self.logger.addHandler(console_handler)

    def log(self, message, log_level=None, **kwargs):
        if log_level:
            self.logger.log(log_level, message, **kwargs)
        else:
            self.logger.info(message, **kwargs)

# arg1:v 数据列表 
# arg2:log_level 日志等级
def dprint(*v, log_level=None):
    times = get_current_times()
    if debug: # 调试模式输出关键check点数据
        print(*v)
    else: # 非调试模式将关键数据记录到日志中
        logger.log(f"Submit{times}, data: {v}", log_level)

def bak_main():
    times = get_current_times()
    bak_main_time = str(datetime.datetime.now()).replace(' ','_')
    if not os.path.exists(bak_source_dir):
        os.makedirs(bak_source_dir)
    if is_cpp_src:
        filename = f"{bak_main_time}_{question_name}_submit{times}_main.cpp"
    else:
        filename = f"{bak_main_time}_{question_name}_submit{times}_main.c"
    cmd = f"cp {target_source_path} {bak_source_dir}/{filename}"
    dprint(cmd)
    exitcode = os.system(cmd)
    if exitcode != 0:
        dprint("bak main error!")
    dprint("bak main success!")


def patch_check(patched_source_path):
    try:
        dprint(f'------------------------- check_patch ------------------------- ')
        git_diff = os.popen("git diff --stat {} {}".format(original_source_path,patched_source_path)).read().strip()
        if git_diff == '':
            dprint("not fix at all so successs")
            return {"status": STATUS_SUCCESS, "msg": "not fix at all so successs"}
        git_diff = git_diff.split('\n')[-1].split(',')
        dprint(f"patch_check.git_diff -> {git_diff}")
        diff_add = 0
        diff_del = 0
        for i in git_diff:
            if 'insertion' in i:
                diff_add = int(re.findall(' (.*?) insertion',i,re.S|re.M)[0])
            elif 'deletion' in i:
                diff_del = int(re.findall(' (.*?) deletion',i,re.S|re.M)[0])
        dprint(f"patch_check.diff_add={diff_add}、diff_del{diff_del}")
        patch_add_limit = 50
        patch_del_limit = 50
        if diff_add > patch_add_limit:
            dprint("patch add too many new lines!")
            return {"status": STATUE_PATCH_LINE_OUT_LIMIT_DOWN, "msg": "patch add too many new lines!"}
        if diff_del > patch_del_limit:
            dprint("patch delete too many lines!")
            return {"status": STATUE_PATCH_LINE_OUT_LIMIT_DOWN, "msg": "patch delete too many lines!"}
        # 自行添加check，失败返回STATUS_DOWN，标志引入新漏洞
        # re1 = os.popen('cat '+patched_source_path+" |grep -A 4 'checkPath(string path)'").read().strip().replace(' ','').replace('\n','')
        # dprint(re1)
        # if 'boolcheckPath(stringpath){if(path.find("..")!=string::npos||path[0]==\'/\'){returnfalse;}' not in re1:
        #     return {"status": STATUS_DOWN, "msg": 'not modify checkPath()!'}
        dprint("patch check success!")
        return {"status": STATUS_SUCCESS, "msg": "good"}
    except Exception as e:
        if debug:
            logger.exception(str(e), exc_info=True)
        dprint(str(e))
        return {"status": STATUS_ERROR, "msg": str(e)}

def compile_and_run(vuln_idx):
    suffix = "c"
    _compile = "gcc"
    import os 
    arg = ''
    if vuln_idx in fsanitize_list:
        arg = '-fsanitize=address'
    if is_cpp_src:
        suffix = "cpp"
        _compile = "g++"
    t = 0
    # 重试三次
    while t < 3:
        try:
            os.system("runuser -u test -- kill -9 -1 1>/dev/null 2/dev/null")
            exitcode = os.system(f'/root/compile_and_run.sh "{arg}" "{debug}" "{suffix}" "{_compile}" "{vuln_idx}" "{gcc_other}"')
            dprint(f'compile cmd: /root/compile_and_run.sh "{arg}" "{debug}" "{suffix}" "{_compile}" "{vuln_idx}" "{gcc_other}"')
            if exitcode != 0:
                dprint("compile error!")
                return  {"status": STATUS_COMPILE_DOWN, "msg": "compile error!"},None
            context.clear(log_level = 'CRITICAL')
            io = process(argv=['chroot','--userspec','test:test', '/', '/tmp/test/run', '/tmp/test/main'],timeout=10)
            if context_debug and vuln_idx in debug_vuln:
                context.clear(log_level = 'debug')
            if not io:
                io.close()
                os.system("runuser -u test -- kill -9 -1 1>/dev/null 2/dev/null")
                return  {"status": STATUS_ERROR, "msg": "connection error"},None
            return  {"status": STATUS_SUCCESS, "msg": "connection ok"},io
        except Exception as e:
            t += 1
            time.sleep(1)
            io.kill()
            io.shutdown()
            dprint(str(e))
        if io:
            io.close()
            io.kill()
            io.shutdown()
        os.system("runuser -u test -- kill -9 -1 1>/dev/null 2/dev/null")
    return  {"status": STATUS_ERROR, "msg": "connection error"},None

def recvuntil_and_check(sh:process, delims):
    result = b''
    for _ in range(0x10000):
        try:
            tmp = sh.recvn(1, timeout=1)
            if tmp != b'':
                result += tmp
                if(result.endswith(delims)):
                    dprint(result)
                    return result
            else:
                break
        except EOFError:
            break

    if not result.endswith(delims):
        raise EOFError
    else:
        dprint(result)
        return result

def sendlineafter_and_check(sh:process, delims, content, drop_enter=False):
    result = b''
    for _ in range(0x10000):
        try:
            tmp = sh.recvn(1, timeout=1)
            if tmp != b'':
                result += tmp
                if(result.endswith(delims)):
                    break
            else:
                break
        except EOFError:
            break

    if not result.endswith(delims):
        raise EOFError
    elif drop_enter:
        sh.send(content)
    else:
        sh.sendline(content)
    dprint(delims,content)


def recvmax_and_check(sh:process, length):
    result = b''
    for _ in range(length):
        try:
            tmp = sh.recvn(1, timeout=1)
            if tmp != b'':
                result += tmp
            else:
                break
        except EOFError:
            break
    dprint(result)
    return result

def recvn_and_check(sh:process, length):
    result = b''
    for _ in range(length):
        try:
            tmp = sh.recvn(1, timeout=1)
            if tmp != b'':
                result += tmp
            else:
                break
        except EOFError:
            break
    if len(result) == length:
        dprint(result)
        return result
    else:
        raise EOFError

check_vul_list = []
def set_check_vul_list(func_list):
    global check_vul_list
    check_vul_list = func_list

# 用户定义函数
def functionality_check():    
    def get_main_pid():
        pid=""
        i=0
        while i<50 and len(pid)==0:
            pid=os.popen("pgrep -r S main").read().strip()
            i+=1
        # error get pid
        if len(pid)==0:
            return 0
        return int(pid)
    def wait_service_online(func):
        def run(sh:process)->map:
            try:
                sh.recvuntil(service_start_tag)
                r=func(sh)
                sh.kill()
                return r
            except Exception as e:
                if debug:
                    dprint(traceback.format_exc())
                sh.kill()
                dprint(str(e))
                return {"status": STATUS_ERROR, "msg": "wait online:"+"panic"}
        return run

    @wait_service_online
    def check_service(sh:process)-> map:
        return check_vul_list[0](sh)

    @wait_service_online
    def check_vul1(sh:process)-> map:
        return check_vul_list[1](sh)

    @wait_service_online
    def check_vul2(sh:process)-> map:
        return check_vul_list[2](sh)

    @wait_service_online
    def check_vul3(sh:process)-> map:
        return check_vul_list[3](sh)

    @wait_service_online
    def check_vul4(sh)-> map:
        return check_vul_list[4](sh)

    @wait_service_online
    def check_vul5(sh)-> map:
        return check_vul_list[5](sh)
    
    check_vuls = [check_service,check_vul1,check_vul2,check_vul3,check_vul4,check_vul5]
    function_check_result=[]
    
    for i in range(len(check_vuls)):
        try:
            if i: 
                dprint(f'------------------------- check_vul{i} ------------------------- ')
            else:
                dprint(f'------------------------- check_service ------------------------- ')
            result,io = compile_and_run(i)
            if result["status"]!=STATUS_SUCCESS or io is None:
                function_check_result.append({"status": STATUS_DOWN, "msg": "connection error"})
                if io:
                    io.close()
                    os.system("runuser -u test -- kill -9 -1 1>/dev/null 2/dev/null")
                continue
            check_vuln_func = check_vuls[i]
            check_func_result = check_vuln_func(io)
            if io:
                io.kill()
                io.shutdown()
                io.close()
            os.system("runuser -u test -- kill -9 -1 1>/dev/null 2/dev/null")
            function_check_result.append(check_func_result)
        except Exception as e:
            if io:
                io.kill()
                io.shutdown()
                io.close()
            dprint(str(e))
            os.system("runuser -u test -- kill -9 -1 1>/dev/null 2/dev/null")
            function_check_result.append( {"status": STATUS_ERROR, "msg": str(e)})

    # must close io
    try:
        if io:
            io.close()
        os.system("runuser -u test -- kill -9 -1 1>/dev/null 2/dev/null")
    except Exception as e:
        pass
    return function_check_result

def _checker():
    check_result_list=[]
    try:
        patch_check_result = patch_check(target_source_path)
        # patch_check行数检测失败,不再检测功能
        # patch_check引入新漏洞检测失败，,不再检测功能
        check_result_list.append(patch_check_result)

        if patch_check_result["status"] !=STATUS_SUCCESS: 
            return check_result_list
        # compile_and_run 
        compile_check_result,io=compile_and_run(0)
        if io:
            io.kill()
            io.shutdown()
            io.close()
        os.system("runuser -u test -- kill -9 -1 1>/dev/null 2/dev/null")
        # bak main source
        bak_main()
        # can't run!!
        check_result_list.append(compile_check_result)
        if compile_check_result["status"]!=STATUS_SUCCESS:
            return check_result_list
        patch_check_result = functionality_check()
        check_result_list+=patch_check_result
        return check_result_list
    except Exception as e:
        if debug:
            traceback.print_exc()
        dprint(str(e))
        check_result_list.append({"status": STATUS_ERROR, "msg": str(e)})
        return check_result_list

def checker():
    ck = _checker()
    # return ck
    # check两次，都错才会真正的down
    for i in ck:
        if i["status"]!=STATUS_SUCCESS:
            return ck
    return ck

# 获取已经执行次数
def get_current_times():
    try:
        f = open('/root/times','rb')
        times=int(f.read())
        f.close()
        return times
    except:
        return  0

# 获取最大执行次数
def init_total_times():
    try:
        f = open('/root/total_times','rb')
        total_times=int(f.read())
        f.close()
        return total_times
    except:
        return 20

def add_times():
    times=get_current_times()
    times+=1
    f = open('/root/times','wb')
    f.write(str(times).encode())
    f.close()
    return times

def sigint_handler(signum, frame):
    os.system("runuser -u test -- kill -9 -1 1>/dev/null 2/dev/null")
    os.system("rm -rf /tmp/test")
    print('Warning: KeyboardInterrupt or AssertionError detected, exiting...')
    dprint('Warning: KeyboardInterrupt or AssertionError detected, exiting...')
    exit(1)

def main():
    try:
        global logger
        signal.signal(signal.SIGINT, sigint_handler)
        logger = CustomLogger()
        times,total_times = get_current_times(),init_total_times()
        if times >= total_times:
            print('Error：程序运行次数已达到上限（{}次）'.format(total_times))
            exit(1)
        times = add_times()
        generate_flag()
        if is_cpp_src: print('提醒：检测程序运行大约15s左右，请耐心等待检测结果。')
        print('提醒：程序已运行次数：{}次；剩余次数：{}次。'.format(times,total_times-times))
        print('漏洞修复结果：')
        result = checker()
        # patch_check出错,没编译过，不进行额外检查
        dprint(result)
        assert(len(result)==1 or len(result)==2 or len(result)==3 or len(result)==8)
        # patch_check返回STATUS_DOWN(题目明确说明不能修改的代码)和STATUS_ERROR（编译过程出现的非预期的异常、连接错误）表示引入新漏洞，并输出原因
        if result[PATCH_CHECK]['status'] == STATUS_DOWN or result[PATCH_CHECK]['status']==STATUS_ERROR:
            print('Error：程序引入新漏洞，请核对修改！')
            print('Msg:',result[PATCH_CHECK]['msg'])
            exit(1)
        elif result[PATCH_CHECK]['status'] == STATUE_PATCH_LINE_OUT_LIMIT_DOWN:
            print('Error：patch 删减的行数超过限制')
            exit(1)
        if result[COMPILE_CHECK]['status']!=STATUS_SUCCESS:
            print('Error：编译失败，请检查')
            exit(1)
        if result[CHECK_SERVICE]['status'] != STATUS_SUCCESS:
            print('Error：代码交互检测异常，请不要修改源程序交互逻辑')
            exit(1)
        
        # [PATCH_CHECK,SERVICE_CHECK,COMPILE_CHECK,Vul1,vul2 ...] 
        # checker中STATUS_SUCCESS表示修复成功、STATUS_DOWN表示没修好、STATUS_ERROR表示服务异常(引入新漏洞)
        # 五个漏洞点如果有某个漏洞流程异常，则报引入新漏洞，退出程序
        for i in range(3,8):
            r=result[i]
            #i-=1
            if r["status"]==STATUS_ERROR:
                print('Error：程序引入新漏洞，请核对修改！')
                print('Msg:',result[i]['msg'])
                exit(1)
        
        # [PATCH_CHECK,SERVICE_CHECK,COMPILE_CHECK,Vul1,vul2 ...]
        for i in range(3,8):
            r=result[i]
            i-=2
            if r["status"]==STATUS_SUCCESS:
                print('（{}）漏洞{}修复正确，flag为{}'.format(i,i,flags[i-1].decode()))
            else:
                print('（{}）漏洞{}修复错误'.format(i,i))
    except (KeyboardInterrupt,AssertionError) as e:
        if debug:
            traceback.print_exc()
        dprint(str(e))
        print('Warning: KeyboardInterrupt or AssertionError detected, exiting...')
        exit(1)
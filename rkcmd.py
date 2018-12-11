import sys
import threading
import subprocess
if sys.version_info.major == 2:
    import commands

threadLock = threading.Lock()


# return (status, result_str)
def __do_command(cmd):
    status = None
    result = None
    threadLock.acquire()
    if sys.version_info.major == 2:
        status, result = commands.getstatusoutput(cmd)
    elif sys.version_info.major == 3:
        status, result = subprocess.getstatusoutput(cmd)
    threadLock.release()
    return status, result


def __get_command_process(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process


def __computer_offset(begin_sec):
    #return hex(int(begin_sec, 16) + 0x2000)
    return hex(int(begin_sec, 16))


def version():
    return __do_command('./rkdeveloptool -v')


def list_device():
    return __do_command('./rkdeveloptool ld')


def reset_device():
    return __do_command('./rkdeveloptool rd')


def download_loader(file):
    print("Downloading Loader " + file)
    return __do_command('./rkdeveloptool db ' + file)


def upgrade_loader(file):
    print("Upgrading Loader " + file)
    return __do_command('./rkdeveloptool ul ' + file)


def write_parameter(file):
    print("Writing Parameter " + file)
    return __do_command('./rkdeveloptool prm ' + file)


def write_lba_bysec(begin_sec, file):
    wt_sec = __computer_offset(begin_sec)
    print("Writing " + begin_sec + "(" + str(wt_sec) + ") " + file)
    return __do_command('./rkdeveloptool wl ' + str(wt_sec) + ' ' + file)


def write_lba_bysec_async(begin_sec, file):
    wt_sec = __computer_offset(begin_sec)
    print("AWriting " + begin_sec + "(" + str(wt_sec) + ") " + file)
    return __get_command_process('./rkdeveloptool wl ' + str(wt_sec) + ' ' + file)


def write_lba_byname(name, file):
    print("Writing " + name + " " + file)
    return __do_command('./rkdeveloptool wlx ' + name + ' ' + file)

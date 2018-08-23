import subprocess
import threading

threadLock = threading.Lock()


# return (status, result_str)
def __do_command(cmd):
    threadLock.acquire()
    status, result = subprocess.getstatusoutput(cmd)
    threadLock.release()
    return status, result


def version():
    return __do_command('rkdeveloptool -v')


def list_device():
    return __do_command('rkdeveloptool ld')


def reset_device():
    return __do_command('rkdeveloptool rd')


def upgrade_loader(file):
    print("Writing Loader " + file)
    return __do_command('rkdeveloptool ul ' + file)


def write_parameter(file):
    print("Writing Parameter " + file)
    return __do_command('rkdeveloptool prm ' + file)


def write_lba_bysec(begin_sec, file):
    print("Writing " + begin_sec + " " + file)
    return __do_command('rkdeveloptool wl ' + begin_sec + ' ' + file)


def write_lba_byname(name, file):
    print("Writing " + name + " " + file)
    return __do_command('rkdeveloptool wlx ' + name + ' ' + file)

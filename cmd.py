import subprocess


# return (status, result_str)
def __do_command(cmd):
    return subprocess.getstatusoutput(cmd)


def version():
    return __do_command('rkdeveloptool -v')


def list_device():
    return __do_command('rkdeveloptool ld')


def reset_device():
    return __do_command('rkdeveloptool rd')

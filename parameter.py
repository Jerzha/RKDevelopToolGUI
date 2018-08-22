import re


class ParameterParser:
    _file = None
    partitions = {}

    def __init__(self, path):
        _file = open(path, mode='r', encoding='utf-8')
        for line in _file:
            print(line.strip())
            if line.startswith('CMDLINE:'):
                self.__parse_cmdline(line)

    def __parse_cmdline(self, line):
        dp = line.split(' ')
        for part in dp[1:]:
            k, v = self.__parse_cmdline_kv(part)
            if k == 'mtdparts':
                self.__parse_cmdline_partitions(v)

    def __parse_cmdline_kv(self, part):
        dp = part.split('=')
        return dp[0], dp[1]

    def __parse_cmdline_partitions(self, partitions):
        dp = partitions.split(',')
        for part in dp:
            siz, addr, name = self.__parse_cmdline_partition_name(part)
            self.partitions[name] = [siz, addr]

    def __parse_cmdline_partition_name(self, partition):
        obj = re.search('(\w+)@(\w+)\((\w+)\)', partition)
        if obj:
            return obj.group(1), obj.group(2), obj.group(3)
        else:
            return None, None, None

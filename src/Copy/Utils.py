#!/usr/bin/env python3

__author__ = 'atul'

import ctypes
import os
import platform
import sys
import errno


class AtUtils:
    @staticmethod
    def get_free_space_mb(folder):
        """ Return folder/drive free space (in MB)
        """
        # Need to check on windows
        if platform.system() == 'Windows':
            free_bytes = ctypes.c_ulonglong(0)
            total = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, ctypes.byref(total),
                                                       ctypes.pointer(free_bytes))
            vol_free = free_bytes.value / 1024 / 1024
            vol_total = total.value / 1024 / 1024
        else:
            st = os.statvfs(folder)
            vol_free = st.f_bavail * st.f_frsize / 1024 / 1024
            vol_total = st.f_frsize * st.f_blocks / 1024 / 1024
        # Return tuple
        return {'free': vol_free, 'total': vol_total}

    @staticmethod
    def mkdir_p(srcpath):
        srcpath = os.path.dirname(srcpath)
        try:
            os.makedirs(srcpath)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(srcpath):
                pass
            else:
                raise

    @staticmethod
    def get_size_to_show(size, unit):

        units = ('B', 'KB', 'MB', 'GB', "TB")

        try:
            count = units.index(unit)
        except ValueError:
            count = 0

        factor = 1024
        length = len(units) - 1
        while factor <= size and count < length:
            size /= factor
            count += 1

        return "{0} {1}".format(size, units[count])


def main(arg):
    a = AtUtils.get_size_to_show(AtUtils.get_free_space_mb('/home/atul')['free'], 'MB')
    print("get_free_space_mb:{0}".format(a))
    print("get_free_space_mb:{0}".format(AtUtils.get_size_to_show(1024, "TB")))


if __name__ == "__main__":
    main(sys.argv)
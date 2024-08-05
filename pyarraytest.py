from array import array
import ctypes
import os
import subprocess
import time
import numpy as np

ctypesptr = ctypes.c_size_t
nome_do_zig = "zigarraytest"
arquivo_zig = f"{nome_do_zig}.zig"
arquivo_zig_dll = f"{nome_do_zig}.dll"

nossa_pasta = os.path.dirname(__file__)
arquivo_zig_full = os.path.normpath(os.path.join(nossa_pasta, arquivo_zig))
arquivo_zig_dll_full = os.path.normpath(os.path.join(nossa_pasta, arquivo_zig_dll))

try:
    cta = ctypes.cdll.LoadLibrary(arquivo_zig_dll_full)
except Exception as e:
    os.chdir(nossa_pasta)
    subprocess.run(
        ["zig", "build-lib", arquivo_zig, "-dynamic", "-O", "ReleaseFast"],
        shell=True,
        env=os.environ,
    )
    time.sleep(1)
    cta = ctypes.cdll.LoadLibrary(arquivo_zig_dll_full)
cta.menor_ou_igual.argtypes = [ctypesptr] * 7
cta.menor_ou_igual.restype = None
menor_ou_igual = cta.menor_ou_igual


def sep_array_py(l, no):
    is_le = []
    is_gt = []
    for i in l:
        if i <= no:
            is_le.append(i)
        else:
            is_gt.append(i)
    return is_le, is_gt


def sep_array_zig_py(a, no):
    l, l_len = a.buffer_info()
    n_array = array("i", [no])
    n, _ = n_array.buffer_info()
    is_le_array = array("i", [0] * l_len)
    is_gt_array = array("i", [0] * l_len)
    resultcounter_is_le_array = array("Q", [0])
    resultcounter_is_gt_array = array("Q", [0])  # usize is 64 bit
    is_le, _ = is_le_array.buffer_info()
    is_gt, _ = is_gt_array.buffer_info()
    resultcounter_is_le, _ = resultcounter_is_le_array.buffer_info()
    resultcounter_is_gt, _ = resultcounter_is_gt_array.buffer_info()
    menor_ou_igual(n, l, l_len, is_le, is_gt, resultcounter_is_le, resultcounter_is_gt)
    return is_le_array[: resultcounter_is_le_array[0]], is_gt_array[
        : resultcounter_is_gt_array[0]
    ]


def sep_array_zig_np(a, no):
    l, l_len = a.ctypes._arr.__array_interface__["data"][0], a.shape[0]
    n_array = np.array([no], dtype="i")
    n = n_array.ctypes._arr.__array_interface__["data"][0]
    is_le_array = np.empty(l_len, dtype="i")
    is_gt_array = np.empty(l_len, dtype="i")
    resultcounter_is_le_array = np.array([0], dtype="Q")
    resultcounter_is_gt_array = np.array([0], dtype="Q")  # usize is 64 bit
    is_le = is_le_array.ctypes._arr.__array_interface__["data"][0]
    is_gt = is_gt_array.ctypes._arr.__array_interface__["data"][0]
    resultcounter_is_le = resultcounter_is_le_array.ctypes._arr.__array_interface__[
        "data"
    ][0]
    resultcounter_is_gt = resultcounter_is_gt_array.ctypes._arr.__array_interface__[
        "data"
    ][0]
    menor_ou_igual(n, l, l_len, is_le, is_gt, resultcounter_is_le, resultcounter_is_gt)
    return is_le_array[: resultcounter_is_le_array[0]], is_gt_array[
        : resultcounter_is_gt_array[0]
    ]


random_array = np.random.randint(-2_000_000_000, 2_000_000_000, 10_000_000, dtype="i")
random_list = random_array.tolist()
a = array("i", random_list)
i = 5
is_le_py, is_gt_py = sep_array_py(random_list, i)
is_le_zig_py, is_gt_zig_py = sep_array_zig_py(a, i)
sep_array_zig_np(random_array, i)


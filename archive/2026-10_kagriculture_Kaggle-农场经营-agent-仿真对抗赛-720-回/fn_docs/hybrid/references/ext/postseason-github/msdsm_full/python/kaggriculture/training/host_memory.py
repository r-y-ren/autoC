"""Small CUDA page-locking wrapper for reusable NumPy transfer buffers."""

from __future__ import annotations

import ctypes
import ctypes.util
from contextlib import suppress
from dataclasses import dataclass

import numpy as np


def _load_cuda_runtime() -> ctypes.CDLL:
    candidates = [ctypes.util.find_library("cudart"), "libcudart.so.12", "libcudart.so"]
    for candidate in candidates:
        if candidate is None:
            continue
        try:
            return ctypes.CDLL(candidate)
        except OSError:
            continue
    raise RuntimeError("CUDA runtime is unavailable; cannot page-lock the host feature buffer")


@dataclass
class RegisteredHostArray:
    array: np.ndarray
    _runtime: ctypes.CDLL
    _closed: bool = False

    def close(self) -> None:
        if self._closed:
            return
        result = self._runtime.cudaHostUnregister(ctypes.c_void_p(self.array.ctypes.data))
        if result != 0:
            raise RuntimeError(f"cudaHostUnregister failed with CUDA error {result}")
        self._closed = True

    def __del__(self) -> None:
        with suppress(RuntimeError):
            self.close()


def register_host_array(array: np.ndarray) -> RegisteredHostArray:
    if not array.flags.c_contiguous:
        raise ValueError("only C-contiguous arrays can be page-locked")
    runtime = _load_cuda_runtime()
    runtime.cudaHostRegister.argtypes = (ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint)
    runtime.cudaHostRegister.restype = ctypes.c_int
    runtime.cudaHostUnregister.argtypes = (ctypes.c_void_p,)
    runtime.cudaHostUnregister.restype = ctypes.c_int
    result = runtime.cudaHostRegister(
        ctypes.c_void_p(array.ctypes.data),
        ctypes.c_size_t(array.nbytes),
        ctypes.c_uint(0),
    )
    if result != 0:
        raise RuntimeError(f"cudaHostRegister failed with CUDA error {result}")
    return RegisteredHostArray(array=array, _runtime=runtime)

"""R11 GSK 预检入口（蓝图 sw-gsk 等价）"""
import sys

from src.build_gsk_prestudy.build_gsk_prestudy import build_gsk_prestudy

if __name__ == "__main__":
    build_gsk_prestudy({})

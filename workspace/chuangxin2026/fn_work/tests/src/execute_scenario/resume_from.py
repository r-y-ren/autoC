# resume_from 桩阶段测试（同名镜像）
import pytest

from src.execute_scenario.resume_from import resume_from


def test_resume_from_stub():
    assert callable(resume_from)
    with pytest.raises(NotImplementedError):
        resume_from(None, [])

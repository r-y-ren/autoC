from src.build_engine_dossier.build_engine_dossier import build_engine_dossier


def test_build_engine_dossier_exists():
    assert callable(build_engine_dossier)

from src.mine_assets.mine_assets import mine_assets


def test_mine_assets_exists():
    assert callable(mine_assets)

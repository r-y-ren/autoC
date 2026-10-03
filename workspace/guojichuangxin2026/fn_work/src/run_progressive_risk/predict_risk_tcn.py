"""TCN 前向：1/3/5/10s 危险概率+剩余安全时间（run_progressive_risk 块）。"""
from __future__ import annotations

HORIZONS = (1, 3, 5, 10)


def _build(channels: int = 16, layers: int = 4):
    import torch
    import torch.nn as nn

    class Block(nn.Module):
        def __init__(self, c, dil):
            super().__init__()
            self.conv1 = nn.Conv1d(c, c, 3, dilation=dil, padding=2 * dil)
            self.conv2 = nn.Conv1d(c, c, 3, dilation=dil, padding=2 * dil)
            self.norm = nn.GroupNorm(1, c)

        def forward(self, x):
            import torch.nn.functional as F
            h = F.relu(self.norm(self.conv1(F.relu(self.norm(x)))))
            h = self.conv2(h)
            return x + h[:, :, : x.shape[2]]

    class Net(nn.Module):
        def __init__(self):
            super().__init__()
            self.inp = nn.Conv1d(len(__import__("run_progressive_risk.build_feature_window", fromlist=["FEATURE_NAMES"]).FEATURE_NAMES) + 1, channels, 1)
            self.blocks = nn.Sequential(*[Block(channels, 2 ** i) for i in range(layers)])
            self.head_prob = nn.Linear(channels, len(HORIZONS))
            self.head_time = nn.Linear(channels, 1)

        def forward(self, x):  # x: [B, T, F]
            import torch
            miss = torch.isnan(x).any(dim=2, keepdim=True).float()      # 缺失指示位
            x = torch.nan_to_num(x, nan=0.0)
            h = self.blocks(self.inp(torch.cat([x, miss], dim=2).transpose(1, 2)))
            pooled = h.mean(dim=2)
            import torch.nn.functional as F
            probs = torch.sigmoid(self.head_prob(pooled))
            time_est = F.softplus(self.head_time(pooled)).squeeze(-1)
            return {"probs": {str(hz): float(probs[0, i]) for i, hz in enumerate(HORIZONS)},
                    "time_to_unsafe_s": float(time_est[0]),
                    "raw": {"probs": probs, "pooled": pooled}}   # 不 detach：训练侧需梯度；推理侧由 no_grad 管

    return Net()


def predict_risk_tcn(features, model):
    """features: [T,F] ndarray（经 build_feature_window）；model: 已加载 Net。"""
    import numpy as np
    import torch
    x = torch.as_tensor(np.asarray(features), dtype=torch.float32).unsqueeze(0)
    if x.shape[1] < 4:
        raise ValueError(f"特征窗过短: {x.shape}")
    with torch.no_grad():
        return model(x)

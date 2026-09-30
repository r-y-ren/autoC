# NOTICE — orderbook_melon_lab（S4 复刻线 S_melon，2026-09-30）

## 移植件署名（Apache-2.0）

- **S_melon 完整形**（`build/s_melon/main.py`）= prvsiyan_melons 整件署名移植。
  - 原作者/件：prvsiyan，Kaggle kernel `prvsiyan/kaggriculture-frontier-the-moon-counts-melons`；
    镜像 `github.com/doanthuan/kaggriculture` `agents/public/prvsiyan_melons.py`。
  - 冻结发现胜者逐字节复刻（sha256 `178ae0f727641cf4b618ebb98ade7aa1a1bed7517281aab9849de82a59d8ed3a`），
    移植仅加注释头（行为零改动）。
  - 许可：Apache-2.0（全文见 `LICENSE-APACHE-2.0.txt`，自源头部逐字抽出）。
  - 上游通知随件逐字保留（源头部）：thomastschinkel、yhay81（shop-router 系列）、destbreso、
    aurax7、tetsutani、prvsiyan、Dmitrii Gluzdov（Two Coins, One Sheep）、Ahmed Berat Ozer
    （V219/V221B/V39 系）、haideptry（2965 master hybrid engine）、sdy623/jaxa623（Beyond 48-0，
    EXP293 sale-advance 机制来源）等；kaggle-environments 1.32.7 引擎抽取件（Apache-2.0）内嵌。
- **混装形**（`build/mix/main.py`）果品件概念移植：
  - 果品件①前跑卖引 ← prvsiyan `Chassis._sell_lead/_front_run/_apply_suppression`（Apache-2.0）。
  - 果品件②终局块重排 ← prvsiyan FRO 尾部再应用模式 + `_v44y_reorder`（Apache-2.0；本混装复用
    c_final 基座内生同核件，零再实现）。基座 c_final 本身属我方 oc_c3/fert60/m13 合建线。

## mooman 概念件口径

mooman E085/E087/E092/E093 系无许可公开件：**未移植、未引用**（面板对战仅作对手装载，
不复制其代码）。如日后参考其"麦先买洗价/路线扫引"概念，一律走干净室重实现并留痕。

## 用法口径

本 lab 产物仅供战役内判决实验（sim_bridge 认证后离线跑局）；不提交、不发射。

## 4. Verify the exact submission entrypoint

Two independent instances are loaded by Kaggle’s actual source loader. Each must produce 719 callbacks, finish all 720 states, and report zero final-ordering errors. This smoke establishes execution; the separately frozen 1,008-game holdout is in section 28.

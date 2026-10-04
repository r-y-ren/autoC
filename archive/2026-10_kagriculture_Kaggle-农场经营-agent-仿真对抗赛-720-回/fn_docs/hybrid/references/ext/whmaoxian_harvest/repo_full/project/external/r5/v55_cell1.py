from pathlib import Path
OUTPUT_ROOT = Path('/kaggle/working') if Path('/kaggle/working').exists() else Path.cwd()
WORKDIR = OUTPUT_ROOT / 'v55_agent'
WORKDIR.mkdir(parents=True, exist_ok=True)
print('Agent directory:', WORKDIR)

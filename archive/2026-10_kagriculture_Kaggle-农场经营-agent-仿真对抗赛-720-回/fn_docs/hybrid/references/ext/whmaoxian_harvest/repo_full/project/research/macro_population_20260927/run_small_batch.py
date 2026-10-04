"""Execute one explicit local test manifest using two worker processes."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import argparse
import arena

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('manifest');parser.add_argument('output')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    manifest=(root/args.manifest).resolve();output=(root/args.output).resolve()
    if manifest.parent!=root or output.parent!=root:raise ValueError('Test files must be inside this research folder')
    with ProcessPoolExecutor(max_workers=2) as pool:
        arena.batch(pool,dict(manifest=str(manifest),output=str(output)))
if __name__=='__main__':main()

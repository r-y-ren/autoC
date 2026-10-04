from pathlib import Path
import ast,json
OUT=Path(__file__).resolve().parent;N=OUT/'notebooks'
files=['aurax7__kaggriculture-shop-router-reactive-v7_1.py.txt',
       'yhay81__shop-router-0909_3.py.txt',
       'leoprovorov__a-song-of-ice-and-fire-fixed-flexible_22.py.txt']
for name in files:
    text=(N/name).read_text(encoding='utf-8')
    if text.startswith('%%writefile '):text=text.split('\n',1)[1]
    tree=ast.parse(text)
    print('\nSOURCE',name,flush=True)
    if name.startswith('aurax7'):
        dest=N/'extracted/aurax';dest.mkdir(exist_ok=True)
        (dest/'main.py').write_text(text,encoding='utf-8')
        print('imports',[ast.unparse(n) for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))],flush=True)
        print('ending',text[-6000:],flush=True)
    else:
        for node in tree.body:
            segment=ast.get_source_segment(text,node)
            if isinstance(node,ast.Assign):
                print('assignment',[ast.unparse(t) for t in node.targets],type(node.value).__name__,len(segment),segment[:100],flush=True)
            elif len(segment)<3000:print(segment,flush=True)

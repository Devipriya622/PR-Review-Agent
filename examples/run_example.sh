#!/usr/bin/env bash
python - <<'PY'
from src.analyzers.python_analyzer import PythonAnalyzer
from src.analyzers.generic_analyzer import GenericAnalyzer
patch=open("tests/sample_diff.patch").read()
lines=patch.splitlines()
filename=None; acc=[]
for l in lines:
    if l.startswith('*** Add File:'): filename=l.split(':',1)[1].strip()
    if l.startswith('+'): acc.append(l)
source_patch="\n".join(acc)
py_an,gen=PythonAnalyzer(),GenericAnalyzer()
print("Python analysis:"); print(py_an.analyze_file(filename,source_patch))
print("Generic analysis:"); print(gen.analyze_file(filename,source_patch))
PY

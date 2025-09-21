# src/analyzers/python_analyzer.py
import ast, subprocess
from radon.complexity import cc_visit, cc_rank
from radon.metrics import h_visit
from src.utils import summarize_lines

class PythonAnalyzer:
    def analyze_file(self, filename: str, patch: str):
        added_lines = [l[1:] for l in patch.splitlines() if l.startswith("+") and not l.startswith("+++")]
        source = "\n".join(added_lines)
        findings = []
        if not source.strip():
            return {"filename": filename,"findings":[{"type":"info","message":"No Python additions"}],"summary": ""}
        try:
            ast.parse(source)
        except SyntaxError as e:
            findings.append({"type":"syntax","severity":"error","message":f"SyntaxError: {e}"})
            return {"filename":filename,"findings":findings,"summary":summarize_lines(added_lines)}
        try:
            blocks = cc_visit(source)
            for b in blocks:
                if b.complexity >= 10:
                    findings.append({"type":"complexity","severity":"warning","message":f"High complexity {b.complexity} in {b.name} line {b.lineno} rank {cc_rank(b.complexity)}"})
        except: pass
        try:
            h_res = h_visit(source)
            mi = h_res.mi if hasattr(h_res,"mi") else None
            if mi and mi < 60:
                findings.append({"type":"maintainability","severity":"warning","message":f"Low maintainability {mi:.1f}"})
        except: pass
        return {"filename":filename,"findings":findings,"summary":summarize_lines(added_lines,20)}

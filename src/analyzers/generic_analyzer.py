# src/analyzers/generic_analyzer.py
from src.utils import extract_language_from_filename, summarize_lines
class GenericAnalyzer:
    def analyze_file(self, filename: str, patch: str):
        findings = []
        added_lines = [l[1:] for l in patch.splitlines() if l.startswith("+") and not l.startswith("+++")]
        removed_lines = [l[1:] for l in patch.splitlines() if l.startswith("-") and not l.startswith("---")]
        num_added, num_removed = len(added_lines), len(removed_lines)
        if num_added + num_removed > 2000:
            findings.append({"type": "size", "severity": "warning", "message": "Large change (over 2000 lines)."})
        tokens = ["TODO","FIXME","HACK","XXX"]
        for i, line in enumerate(patch.splitlines()):
            for t in tokens:
                if t in line:
                    findings.append({"type": "todo","severity":"info","message":f"Found marker {t} line {i+1}: {line.strip()}"})
        lang = extract_language_from_filename(filename)
        return {"filename": filename,"language": lang,"num_added": num_added,"num_removed": num_removed,"findings": findings,"patch_sample": summarize_lines(patch.splitlines(),8)}

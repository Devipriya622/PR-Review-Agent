# src/analyzers/scoring.py
def score_pr(pr_analysis):
    score = 100
    for f in pr_analysis.get("file_reports", []):
        for item in f.get("findings", []):
            sev = item.get("severity","info")
            if sev == "error": score -= 20
            elif sev == "warning": score -= 8
            elif sev == "info": score -= 1
    nf = len(pr_analysis.get("file_reports", []))
    if nf > 10: score -= (nf-10)*2
    score = max(0, score)
    pr_analysis["score"] = score
    return pr_analysis

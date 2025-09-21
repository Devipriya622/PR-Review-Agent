# src/reporters/json_reporter.py
import json
class JSONReporter:
    def report(self, pr_meta, analysis):
        out = {"pr":{"title":pr_meta.get("title"),"author":pr_meta.get("author"),"url":pr_meta.get("url")},"score":analysis.get("score"),"files":analysis.get("file_reports",[])}
        print(json.dumps(out,indent=2,ensure_ascii=False))

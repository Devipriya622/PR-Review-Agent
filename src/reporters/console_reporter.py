# src/reporters/console_reporter.py
import textwrap
def _print_item(i): print(f"- [{i.get('severity','info').upper()}] {i.get('message')}")
class ConsoleReporter:
    def report(self, pr_meta, analysis):
        print("="*80)
        print(f"PR: {pr_meta.get('title')} by {pr_meta.get('author')}")
        print(f"URL: {pr_meta.get('url')}")
        print("-"*80)
        print(f"Overall score: {analysis.get('score')}/100")
        print("-"*80)
        for fr in analysis.get("file_reports", []):
            print(f"File: {fr.get('filename')} (+{fr.get('num_added')} -{fr.get('num_removed')}) lang={fr.get('language')}")
            if fr.get("summary"):
                print("Summary of added code:")
                print(textwrap.indent(fr.get("summary"),"    "))
            if fr.get("findings"):
                print("Findings:")
                for it in fr.get("findings"): _print_item(it)
            print("-"*40)
        print("End of report")
        print("="*80)

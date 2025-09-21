# src/cli.py
import argparse, sys
from src.config import Config
from fetchers.github_fetcher import GitHubFetcher
from fetchers.gitlab_fetcher import GitLabFetcher
from fetchers.bitbucket_fetcher import BitbucketFetcher
from analyzers import PythonAnalyzer, GenericAnalyzer, score_pr
from reporters import ConsoleReporter, JSONReporter

def choose_fetcher(kind,args):
    kind=kind.lower()
    if kind=="github": return GitHubFetcher(token=args.token)
    if kind=="gitlab": return GitLabFetcher(token=args.token, base_url=args.base_url)
    if kind=="bitbucket": return BitbucketFetcher(username=args.username, app_password=args.app_password)
    raise ValueError("Unsupported kind")

def analyze_pr(pr_meta):
    python_an, gen_an = PythonAnalyzer(), GenericAnalyzer()
    file_reports=[]
    for f in pr_meta.get("files", []):
        filename, patch = f.get("filename"), f.get("patch","") or ""
        lang = gen_an.analyze_file(filename, patch).get("language")
        if lang=="python":
            pa, ga = python_an.analyze_file(filename,patch), gen_an.analyze_file(filename,patch)
            merged={"filename":filename,"language":lang,"num_added":ga.get("num_added"),"num_removed":ga.get("num_removed"),"findings":(pa.get("findings",[]))+(ga.get("findings",[])),"summary":pa.get("summary") or ga.get("patch_sample","")}
        else:
            ga = gen_an.analyze_file(filename,patch)
            merged={"filename":filename,"language":ga.get("language"),"num_added":ga.get("num_added"),"num_removed":ga.get("num_removed"),"findings":ga.get("findings",[]),"summary":ga.get("patch_sample","")}
        file_reports.append(merged)
    analysis={"file_reports":file_reports}
    return score_pr(analysis)

def main(argv=None):
    parser=argparse.ArgumentParser(prog="pr-review-agent")
    parser.add_argument("--kind",required=True,choices=["github","gitlab","bitbucket"])
    parser.add_argument("--repo",required=True)
    parser.add_argument("--pr",required=True)
    parser.add_argument("--token",default=None)
    parser.add_argument("--base-url",default="https://gitlab.com")
    parser.add_argument("--username",default=None)
    parser.add_argument("--app-password",default=None)
    parser.add_argument("--json",action="store_true")
    args=parser.parse_args(argv)
    fetcher=choose_fetcher(args.kind,args)
    try: pr_meta=fetcher.fetch_pr(args.repo,args.pr)
    except Exception as e: print("Error fetching PR:",e); return 2
    analysis=analyze_pr(pr_meta)
    reporter=JSONReporter() if args.json else ConsoleReporter()
    reporter.report(pr_meta,analysis)
    return 0

if __name__=="__main__": sys.exit(main())

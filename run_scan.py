from pathlib import Path
import subprocess, json, time, datetime, hashlib
ROOT=Path(__file__).resolve().parent
JAVA=next((ROOT/'tools'/'java').glob('*/bin/java.exe'))
JAR=ROOT/'tools'/'apache-rat-0.18'/'apache-rat-0.18.jar'
SOURCE=ROOT/'source'/'commons-cli-1.11.0-src'
E=ROOT/'evidence'
def run(label,args):
    start=time.perf_counter()
    p=subprocess.run([str(JAVA),*args],cwd=ROOT,capture_output=True)
    (E/(label+'.stdout.txt')).write_bytes(p.stdout)
    (E/(label+'.stderr.txt')).write_bytes(p.stderr)
    r={'label':label,'command':['java',*args],'exit_code':p.returncode,'duration_seconds':round(time.perf_counter()-start,3),'timestamp':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()}
    print(json.dumps(r,ensure_ascii=False),flush=True)
    return r
results=[run('java-version',['-version']),run('rat-help',['-jar',str(JAR),'--help'])]
manifest={p.relative_to(SOURCE).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(SOURCE.rglob('*')) if p.is_file()}
(E/'source-manifest.json').write_text(json.dumps(manifest,indent=2))
for style,ext in [('plain-rat','txt'),('xml','xml')]:
    results.append(run('baseline-'+ext,['-jar',str(JAR),'--output-style',style,'--output-file',str(E/('rat-baseline.'+ext)),str(SOURCE)]))
(E/'runs.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
assert manifest=={p.relative_to(SOURCE).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(SOURCE.rglob('*')) if p.is_file()}
print('Source unchanged; files:',len(manifest))

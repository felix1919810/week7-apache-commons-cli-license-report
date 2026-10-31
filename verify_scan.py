from pathlib import Path
import json, subprocess, hashlib, time, datetime, xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent; E=R/'evidence'; S=R/'source'/'commons-cli-1.11.0-src'
java=next((R/'tools'/'java').glob('*/bin/java.exe'));jar=R/'tools'/'apache-rat-0.18'/'apache-rat-0.18.jar'
original=(S/'src/main/java/org/apache/commons/cli/AlreadySelectedException.java').read_bytes()
cases={'positive':('AlreadySelectedException.java',original),'missing-header':('AlreadySelectedException.java',original.split(b'*/',1)[1].lstrip()),'restored-header':('AlreadySelectedException.java',original),'cgi-text-review':('download_cli.txt',(S/'src/site/resources/download_cli.cgi').read_bytes())}
runs=[]
for label,(name,data) in cases.items():
    folder=R/'controls'/label;folder.mkdir(parents=True,exist_ok=True);(folder/name).write_bytes(data)
    report=E/f'rat-{label}.xml';args=[str(java),'-jar',str(jar),'--output-style','xml','--output-file',str(report),str(folder)]
    start=time.perf_counter();p=subprocess.run(args,cwd=R,capture_output=True)
    (E/f'{label}.stdout.txt').write_bytes(p.stdout);(E/f'{label}.stderr.txt').write_bytes(p.stderr)
    parsed=ET.parse(report).getroot();resources=[{'file':x.get('name'),'type':x.get('type'),'licenses':[dict(z.attrib) for z in x.findall('license')]} for x in parsed.findall('resource')]
    runs.append({'case':label,'exit_code':p.returncode,'duration_seconds':round(time.perf_counter()-start,3),'resources':resources,'timestamp':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'input_sha256':hashlib.sha256(data).hexdigest()})
    print(json.dumps(runs[-1]),flush=True)
baseline=ET.parse(E/'rat-baseline.xml').getroot();resources=baseline.findall('resource');manifest=json.loads((E/'source-manifest.json').read_text())
assert {x.get('name').lstrip('/') for x in resources}==set(manifest)
java_resources=[x for x in resources if x.get('name').endswith('.java')]
assert len(java_resources)==87 and all(x.get('type')=='STANDARD' and any(z.get('id')=='AL2.0' and z.get('approval')=='true' for z in x.findall('license')) for x in java_resources)
assert manifest=={p.relative_to(S).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in S.rglob('*') if p.is_file()}
summary={'file_count':len(resources),'java_count':len(java_resources),'all_java_files_approved':True,'standard_count':sum(x.get('type')=='STANDARD' for x in resources),'binary_count':sum(x.get('type')=='BINARY' for x in resources),'notice_count':sum(x.get('type')=='NOTICE' for x in resources),'source_unchanged':True,'all_source_paths_accounted_for':True,'cgi_exit_reason':'No standard files or recognized license categories/names; not an unapproved-license detection. The unchanged-byte .txt copy remains BINARY.','controls':runs}
(E/'verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
assert runs[0]['exit_code']==0 and runs[1]['exit_code']!=0 and runs[2]['exit_code']==0 and runs[3]['exit_code']!=0

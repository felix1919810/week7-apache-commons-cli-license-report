from pathlib import Path
import urllib.request, json, hashlib, zipfile, concurrent.futures
ROOT=Path(__file__).resolve().parent
for folder in ['tools','evidence','source']:(ROOT/folder).mkdir(parents=True,exist_ok=True)
def get(url,path):
    req=urllib.request.Request(url,headers={'User-Agent':'license-homework-test'})
    with urllib.request.urlopen(req,timeout=120) as r: data=r.read()
    path.write_bytes(data)
    print(path.name,len(data),flush=True)
    return data
def apache(name,url,dest):
    p=ROOT/'tools'/name
    data=get(url,p); expected=get(url+'.sha512',p.with_name(name+'.sha512')).decode().strip().split()[0]
    actual=hashlib.sha512(data).hexdigest()
    assert actual.lower()==expected.lower(),(name,actual,expected)
    with zipfile.ZipFile(p) as z:z.extractall(ROOT/dest)
    return {'name':name,'url':url,'sha512':actual,'verified':True}
def java():
    url='https://api.adoptium.net/v3/assets/latest/17/hotspot?architecture=x64&image_type=jre&os=windows&vendor=eclipse'
    meta=json.loads(get(url,ROOT/'tools'/'java-download.json'))[0]['binary']['package']
    p=ROOT/'tools'/'java.zip'; data=get(meta['link'],p)
    assert hashlib.sha256(data).hexdigest()==meta['checksum']
    with zipfile.ZipFile(p) as z:z.extractall(ROOT/'tools'/'java')
    return {'name':meta['name'],'url':meta['link'],'sha256':meta['checksum'],'verified':True}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    jobs=[pool.submit(java),pool.submit(apache,'apache-rat-0.18-bin.zip','https://archive.apache.org/dist/creadur/apache-rat-0.18/apache-rat-0.18-bin.zip','tools'),pool.submit(apache,'commons-cli-1.11.0-src.zip','https://archive.apache.org/dist/commons/cli/source/commons-cli-1.11.0-src.zip','source')]
    result=[j.result() for j in jobs]
(ROOT/'evidence'/'downloads.json').write_text(json.dumps(result,indent=2),encoding='utf-8')

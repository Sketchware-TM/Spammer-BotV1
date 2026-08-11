#!/usr/bin/env/python3
import sys,os,base64,hashlib,random,string,re
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

def g(p,s=None):
 if s is None:s=get_random_bytes(16)
 k=hashlib.pbkdf2_hmac('sha256',p.encode(),s,1000,dklen=32)
 iv=get_random_bytes(16)
 return k,iv,s

def e(d,p):
 k,iv,s=g(p)
 c=AES.new(k,AES.MODE_CBC,iv)
 en=c.encrypt(pad(d,AES.block_size))
 return en,iv,s,k

def x(d,k=None):
 if k is None:k=get_random_bytes(32)
 r=bytearray(d)
 for i in range(len(r)):r[i]^=k[i%len(k)]
 rk=k[::-1]
 for i in range(len(r)):r[i]^=rk[i%len(rk)]
 return bytes(r),k

def o(c,p):
 en,iv,s,key=e(c.encode(),p)
 xd,xk=x(en)
 cmb=s+iv+xk+xd
 b64=base64.b64encode(cmb).decode()
 kh=key.hex()
 ih=iv.hex()
 return b(b64,kh,ih)

def b(d,kh,ih):
 v={ 'd':''.join(random.choices(string.ascii_lowercase,k=8)),'p':''.join(random.choices(string.ascii_lowercase,k=8)),'x':''.join(random.choices(string.ascii_lowercase,k=10)),'r':''.join(random.choices(string.ascii_lowercase,k=8)) }
 return f'''<!DOCTYPE html> <!-- ENC BY Sketchware-TM -->
<html>
<head><meta charset="UTF-8"><title>Protected</title>
<style>body{{margin:0;background:#0a0a0a;display:flex;justify-content:center;align-items:center;height:100vh;font-family:monospace;color:#00ff00;}}</style>
</head>
<body>
<div id="c" style="padding:20px;max-width:800px;word-wrap:break-word;"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
<script>
(function(){{
if(typeof CryptoJS==='undefined'){{document.getElementById('c').innerHTML='<h1 style="color:red;">Error: CryptoJS gagal dimuat</h1>';return;}}
var t0=performance.now();debugger;var t1=performance.now();if(t1-t0>100){{document.body.innerHTML='<h1 style="color:red;text-align:center;margin-top:20%;">🔒</h1>';return;}}
var {v['d']}=function(s){{return s.split('').reverse().join('');}};
var {v['p']}='encoded';if({v['d']}('dedocne')!=='encoded'){{document.write('<h1>Tamper</h1>');return;}}
function {v['x']}(data,keyHex,ivHex){{
var b=atob(data),u=new Uint8Array(b.length);for(var i=0;i<b.length;i++)u[i]=b.charCodeAt(i);
var s=u.slice(0,16),iv=u.slice(16,32),xk=u.slice(32,64),en=u.slice(64);
var xd=new Uint8Array(en.length),rk=new Uint8Array(xk);rk.reverse();
for(var i=0;i<en.length;i++)xd[i]=en[i]^rk[i%rk.length];
var xd2=new Uint8Array(xd.length);for(var i=0;i<xd.length;i++)xd2[i]=xd[i]^xk[i%xk.length];
var key=CryptoJS.enc.Hex.parse(keyHex);
var ivWord=CryptoJS.enc.Hex.parse(ivHex);
var cipherHex=Array.from(xd2).map(b=>b.toString(16).padStart(2,'0')).join('');
var cipherWord=CryptoJS.enc.Hex.parse(cipherHex);
var dec=CryptoJS.AES.decrypt({{ciphertext:cipherWord}},key,{{iv:ivWord,mode:CryptoJS.mode.CBC,padding:CryptoJS.pad.Pkcs7}});
return dec.toString(CryptoJS.enc.Utf8);
}}
try{{var html={v['x']}('{d}','{kh}','{ih}');
var container=document.getElementById('c');
container.innerHTML=html.replace(/<script[\\s\\S]*?>[\\s\\S]*?<\\/script>/gi,'');
var scripts=html.match(/<script[\\s\\S]*?>([\\s\\S]*?)<\\/script>/gi);
if(scripts){{scripts.forEach(function(s){{var c=s.replace(/<script[\\s\\S]*?>/,'').replace(/<\\/script>/,'');try{{eval(c);}}catch(e){{console.error('Script error:',e);}}}});}}
}}catch(e){{document.getElementById('c').innerHTML='<h1>Error: '+e.message+'</h1>';}}
}})();
</script>
</body>
</html>'''

def main():
 if len(sys.argv)<3:
  print("Usage: python3 obf_html.py <input.html> <output.html> [password]")
  sys.exit(1)
 f=sys.argv[1]; oo=sys.argv[2]; p=sys.argv[3] if len(sys.argv)>3 else "SkTerminalOn"
 if not os.path.exists(f): print("[-] File not found"); sys.exit(1)
 with open(f,'r',encoding='utf-8') as file: c=file.read()
 print("[+] Obfuscating v1.0.1")
 res=o(c,p)
 with open(oo,'w',encoding='utf-8') as file: file.write(res)
 print(f"[+] Done: {oo}")

if __name__=="__main__": main()

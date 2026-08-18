#!/usr/bin/env python3
import sys
import os
import base64
import hashlib
import random
import string
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

PBKDF2_ITER = 150000
SALT_LEN = 16
NONCE_LEN = 12
CHUNK_COUNT = 16

def check_debug():
    if sys.gettrace() is not None:
        print("[!] Debugger detected! Exiting.")
        sys.exit(1)
    if os.environ.get('PYCHARM_HOSTED') is not None:
        print("[!] IDE debugger detected! Exiting.")
        sys.exit(1)
    if os.environ.get('PYTHONDEBUG') is not None:
        print("[!] Python debug mode detected! Exiting.")
        sys.exit(1)

def derive_key(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, PBKDF2_ITER, dklen=32)

def encrypt_content(content, master_pass):
    salt = get_random_bytes(SALT_LEN)
    key = derive_key(master_pass, salt)
    nonce = get_random_bytes(NONCE_LEN)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(content.encode('utf-8'))
    return ciphertext, tag, nonce, salt

def chunk_and_shuffle(text, n):
    size = -(-len(text) // n)
    chunks = [text[i:i+size] for i in range(0, len(text), size)]
    while len(chunks) < n:
        chunks.append('')
    order = list(range(len(chunks)))
    random.shuffle(order)
    shuffled = [chunks[i] for i in order]
    return shuffled, order

def build_html(ciphertext, tag, nonce, salt, master_pass, content_hash):
    salt_b64 = base64.b64encode(salt).decode()
    nonce_b64 = base64.b64encode(nonce).decode()
    ciphertext_b64 = base64.b64encode(ciphertext).decode()
    tag_b64 = base64.b64encode(tag).decode()

    shuffled_pass, order_pass = chunk_and_shuffle(master_pass, CHUNK_COUNT)
    b64_chunks = [base64.b64encode(c.encode()).decode() for c in shuffled_pass]
    order_pass_str = '[' + ','.join(map(str, order_pass)) + ']'

    pvar = ''.join(random.choices(string.ascii_lowercase, k=8))
    ovar = ''.join(random.choices(string.ascii_lowercase, k=8))

    js = f'''\
(async function() {{
try {{
    var {pvar}=[{', '.join([f'atob("{c}")' for c in b64_chunks])}];
    var {ovar}={order_pass_str};
    var originalPass=[];
    {ovar}.forEach(function(o,idx){{originalPass[o]={pvar}[idx];}});
    var pass=originalPass.join('');
    var saltB64="{salt_b64}";
    var nonceB64="{nonce_b64}";
    var cipherB64="{ciphertext_b64}";
    var tagB64="{tag_b64}";
    var iterations={PBKDF2_ITER};

    function b64ToArrayBuffer(b64) {{
        var binary = atob(b64);
        var bytes = new Uint8Array(binary.length);
        for (var i = 0; i < binary.length; i++) {{
            bytes[i] = binary.charCodeAt(i);
        }}
        return bytes.buffer;
    }}

    var salt = b64ToArrayBuffer(saltB64);
    var nonce = b64ToArrayBuffer(nonceB64);
    var ciphertext = b64ToArrayBuffer(cipherB64);
    var tag = b64ToArrayBuffer(tagB64);

    var combined = new Uint8Array(ciphertext.byteLength + tag.byteLength);
    combined.set(new Uint8Array(ciphertext), 0);
    combined.set(new Uint8Array(tag), ciphertext.byteLength);

    var enc = new TextEncoder();
    var keyMaterial = await crypto.subtle.importKey(
        'raw', enc.encode(pass), 'PBKDF2', false, ['deriveKey']
    );
    var key = await crypto.subtle.deriveKey(
        {{
            name: 'PBKDF2',
            salt: salt,
            iterations: iterations,
            hash: 'SHA-256'
        }},
        keyMaterial,
        {{ name: 'AES-GCM', length: 256 }},
        false,
        ['decrypt']
    );

    var plaintext = await crypto.subtle.decrypt(
        {{ name: 'AES-GCM', iv: nonce, tagLength: 128 }},
        key,
        combined
    );
    var html = new TextDecoder('utf-8').decode(plaintext);

    if (!html || html.length === 0) throw new Error('Decryption failed - wrong password?');

    var hashBuffer = await crypto.subtle.digest('SHA-256', enc.encode(html));
    var hashArray = Array.from(new Uint8Array(hashBuffer));
    var hashHex = hashArray.map(b => ('0' + b.toString(16)).slice(-2)).join('');
    if (hashHex !== "{content_hash}") {{
        document.getElementById('c').innerHTML = '<span style="color:#ff0000;">Error: Content tampered!</span>';
        throw new Error('Integrity check failed');
    }}

    document.getElementById('c').innerHTML = html.replace(/<script[\\s\\S]*?>[\\s\\S]*?<\\/script>/gi, '');
}} catch(e) {{
    document.getElementById('c').innerHTML = '<span style="color:#ff0000;">Error: ' + e.message + '</span>';
    console.error('Decryption error:', e);
}}
}})();
'''

    html = rf'''<!DOCTYPE html> <!-- OBFUSCATE BY @SkOfficialAccount29 -->
<html><head><meta charset="UTF-8"><title>Protected</title>
<style>body{{margin:0;background:#0a0a0a;display:flex;justify-content:center;align-items:center;height:100vh;font-family:monospace;color:#00ff00;}}#c{{max-width:90%;max-height:90%;overflow:auto;padding:20px;}}</style>
</head><body><div id="c">Loading...</div>
<script>{js}</script></body></html>'''
    return html

def main():
    check_debug()
    if len(sys.argv) < 4:
        print("Usage: python3 obf_html_aesgcm.py <input.html> <output.html> <password>")
        sys.exit(1)
    infile = sys.argv[1]
    outfile = sys.argv[2]
    password = sys.argv[3]

    if not os.path.exists(infile):
        print("[-] File not found")
        sys.exit(1)
    if len(password) < 4:
        print("[-] Password too short (min 4 characters)")
        sys.exit(1)

    with open(infile, 'r', encoding='utf-8') as f:
        content = f.read()

    content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
    ciphertext, tag, nonce, salt = encrypt_content(content, password)
    result = build_html(ciphertext, tag, nonce, salt, password, content_hash)

    with open(outfile, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"[+] Done: {outfile}")
    print(f"[i] Password: {password}")

if __name__ == "__main__":
    main()
# python obfuscate html
import sys, os
import base64

def obfuscate(content):
    # Encode to base64
    b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    # Convert each char to hex escape sequence
    hex_str = ''.join(f'\\x{ord(c):02x}' for c in b64)
    return hex_str

def generate_html(original_html, output_file):
    obf = obfuscate(original_html)
    html_template = f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Protected Html</title></head>
<body>
  <script>
    !function() {{
      var encoded = ['{obf}'];
      var decodedString = encoded[0].replace(/\\\\x([0-9a-f]{{2}})/gi, function(match, hex) {{
        return String.fromCharCode(parseInt(hex, 16));
      }});
      var decodedBase64 = atob(decodedString);
      document.open();
      document.write(decodedBase64);
      document.close();
    }}()
  </script>
</body>
</html>'''
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"[+] Self-decoding HTML saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python html_obfuscator_selfdecode.py <input.html> <output.html>")
        sys.exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        content = f.read()
    generate_html(content, sys.argv[2])

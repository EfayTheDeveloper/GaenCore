import sys
import re

dict = {
    '@': "document.getElementById",
    "adopt": "appendChild",
    "muted": "const"
}

if len(sys.argv) < 2:
    print("Kullanım: eyc dosya.eyc veya eyc index dosya.js dosya.html")
    sys.exit(1)
elif sys.argv[1] == "index":
    file = open(sys.argv[3], "w", encoding="utf-8")
    file.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
</head>
<body>
    <div id="root"></div>
    <script src="{sys.argv[2]}"></script>
</body>
</html>
""")
    file.close()
else:
    input_file = sys.argv[1]
    if not input_file.endswith(".eyc"):
        print("Hata: Sadece .eyc dosyaları işlenebilir!")
        sys.exit(1)

    output_file = input_file.replace(".eyc", ".js")

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'@|\b(?:muted|adopt)\b'

    def repl(match):
        token = match.group(0)
        return dict.get(token, token)

    converted = re.sub(pattern, repl, content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(converted)

    print(f"{output_file} başarıyla oluşturuldu.")

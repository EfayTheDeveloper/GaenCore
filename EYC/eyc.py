from sys import argv
import os
import re

if len(argv) > 1:
    if argv[1] == "built":
        if len(argv) > 4 and argv[2] == "-i":
            file = open(argv[4], "w", encoding="utf-8")
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
    <script src="{argv[3]}"></script>
</body>
</html>
""")
            file.close()

    elif argv[1] == "-c":
        filename = argv[2]
        if filename.endswith(".eyc"):
            output_name = os.path.splitext(filename)[0] + ".js"
            
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()

            compiled_lines = []
            for line in lines:
                new_line = line
                
                if "@tt" in new_line:
                    pattern = r"@tt\s+([\w\.]+?\(.*?\)),\s*([\w\.]+)"
                    replacement = r"\2.trigA(); \1; \2.trigB();"
                    new_line = re.sub(pattern, replacement, new_line)

                if "#c-ne" in new_line:
                    new_line = new_line.replace("#c-ne", "const")
                
                new_line = new_line.replace("elements.", "document.")
                new_line = new_line.replace(".adopt(", ".appendChild(")
                new_line = new_line.replace("@root", 'document.getElementById("root")')
                
                compiled_lines.append(new_line)

            with open(output_name, "w", encoding="utf-8") as f:
                f.writelines(compiled_lines)

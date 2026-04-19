import os

categories = [
    "Phishing",
    "Malware",
    "Brute-Force",
    "Data-Exfiltration",
    "False-Positives"
]

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>SOC Dashboard</title>

<style>
body {
    font-family: Arial;
    background: #0d1117;
    color: #c9d1d9;
    padding: 20px;
}
h1 { color: #58a6ff; }

.case-link {
    display: block;
    margin: 6px 0;
    cursor: pointer;
}

.tp { color: #3fb950; }
.fp { color: #8b949e; }

#viewer {
    margin-top: 25px;
    padding: 20px;
    border: 1px solid #30363d;
    background: #161b22;
}

img {
    max-width: 100%;
    margin-top: 15px;
    border: 1px solid #30363d;
}
</style>
</head>

<body>

<h1>📊 SOC Analyst Dashboard</h1>

<div id="viewer">
<h2>Case Viewer</h2>
<div id="content">Click a case to view</div>
</div>

<script>
function loadCase(path) {
    fetch(path)
    .then(res => res.text())
    .then(data => {

        let html = data
            .replace(/\\n/g, "<br>")
            .replace(/\\*\\*(.*?)\\*\\*/g, "<b>$1</b>");

        // Detect image
        const match = data.match(/!\\[.*?\\]\\((.*?)\\)/);
        if (match) {
            html += "<br><img src='" + path.replace(/[^/]+$/, '') + match[1] + "'>";
        }

        document.getElementById("content").innerHTML = html;
    })
    .catch(err => {
        document.getElementById("content").innerHTML = "Error loading file";
        console.error(err);
    });
}
</script>
"""

# ===== GENERATE CASE LIST =====
for category in categories:
    if os.path.exists(category):

        html += f"<h2>{category}</h2>"

        files = [f for f in os.listdir(category) if f.endswith(".md")]
        files.sort(reverse=True)

        for file in files:
            path = f"{category}/{file}"

            html += f'''
<div class="case-link" onclick="loadCase('{path}')">
    {file}
</div>
'''

html += "</body></html>"

with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Dashboard updated")
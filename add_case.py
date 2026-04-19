import os
import shutil
import datetime
import re
from tkinter import Tk, filedialog

try:
    # ===== CATEGORY SELECTION =====
    # Dictionary mapping user input to folder names
    categories = {
        "1": "Phishing",
        "2": "Malware",
        "3": "Brute-Force",
        "4": "Data-Exfiltration",
        "5": "False-Positives"
    }

    print("\nSelect Category:")
    for key, value in categories.items():
        print(f"{key}. {value}")

    choice = input("Enter number: ").strip()

    # Validate user input
    if choice not in categories:
        print("Invalid option")
        input("Press Enter to exit...")
        exit()

    category = categories[choice]

    # ===== USER INPUT =====
    # Collect core SOC analysis fields
    title = input("Title: ").strip()
    verdict = input("Verdict (TP/FP): ").strip()
    reason = input("Reason: ").strip()
    action = input("Action: ").strip()

    # ===== SCREENSHOT SELECTION =====
    # Open file dialog to optionally select evidence screenshot
    root = Tk()
    root.withdraw()

    print("\nSelect screenshot (cancel if none)...")
    screenshot_path = filedialog.askopenfilename()

    # ===== AUTO FILE NAMING =====
    # Normalize title into a clean filename format
    def clean_filename(text):
        text = text.lower()
        text = re.sub(r'[^a-z0-9]+', '_', text)
        return text.strip('_')

    date = datetime.datetime.now().strftime("%Y%m%d")
    filename = f"{date}_{clean_filename(title)}"

    # ===== DIRECTORY CREATION =====
    # Ensure category folder exists
    os.makedirs(category, exist_ok=True)
    file_path = f"{category}/{filename}.md"

    # ===== IMAGE PROCESSING =====
    # Copy screenshot and rename it to match the case filename
    image_md = ""
    if screenshot_path:
        if os.path.exists(screenshot_path):
            ext = os.path.splitext(screenshot_path)[1]
            img_name = f"{filename}{ext}"
            dest_path = os.path.join(category, img_name)

            shutil.copy(screenshot_path, dest_path)

            image_md = f"\n![evidence]({img_name})\n"
        else:
            print("Screenshot not found, skipping image")

    # ===== MARKDOWN CONTENT =====
    # SOC-style case documentation
    content = f"""# {title}

**Verdict:** {verdict}

**Reason:**  
{reason}

**Action:**  
{action}
{image_md}
"""

    # ===== WRITE FILE =====
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nCreated: {file_path}")

    # ===== UPDATE DASHBOARD =====
    # Rebuild index file with all cases
    os.system("python update_index.py")

    # ===== GIT OPERATIONS =====
    # Stage, commit and push changes to GitHub
    if os.path.exists(".git"):
        print("\nUploading to GitHub...")
        os.system("git add .")
        os.system(f'git commit -m "Add case + update index: {title}"')
        os.system("git push")
        print("Uploaded successfully")
    else:
        print("Not inside a git repository")

    input("\nPress Enter to exit...")

except Exception as e:
    print(f"\nERROR: {e}")
    input("Press Enter to exit...")
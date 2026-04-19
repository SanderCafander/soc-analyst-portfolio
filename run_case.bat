@echo off

python add_case.py
python update_index.py

git add .
git commit -m "New SOC case"
git push

pause
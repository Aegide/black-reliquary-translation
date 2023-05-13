# clear;sh bin/localization.sh
python bin/main.py
cp build/*.xml /c/'Program Files (x86)'/Steam/steamapps/common/'Black Reliquary'/localization
(cd /c/'Program Files (x86)'/Steam/steamapps/common/'Black Reliquary'/_windows && ./localization.exe) > build.txt
cat build.txt
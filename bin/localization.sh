# clear;sh bin/localization.sh

python bin/main.py

cp build/*.xml /c/'Program Files (x86)'/Steam/steamapps/common/'Black Reliquary'/localization

(cd /c/'Program Files (x86)'/Steam/steamapps/common/'Black Reliquary'/_windows && ./localization.exe) > build.txt

echo " "
echo "---------------------------------"
echo " "

cat build.txt | grep -v "SUCCESS!"

cp /c/'Program Files (x86)'/Steam/steamapps/common/'Black Reliquary'/localization/missing_strings.csv missing_strings.csv

cat missing_strings.csv | grep -v ",PSN," | grep -v ",switch," | grep -v ",xb1,"

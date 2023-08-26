# clear;sh bin/localization.sh

echo " "
echo ">> CLEANING"
echo " "

rm review/*.xml
rm build/*.xml
echo "" > "/c/Program Files (x86)/Steam/steamapps/common/Black Reliquary/localization/missing_strings.csv"

echo " "
echo ">> LOCALIZING"
echo " "

python bin/main.py

echo " "
echo " "
echo ">> BUILDING"
echo " "

cp build/*.xml /c/'Program Files (x86)'/Steam/steamapps/common/'Black Reliquary'/localization
(cd "/c/Program Files (x86)/Steam/steamapps/common/Black Reliquary/_windows" && ./localization.exe) > build.txt
cat build.txt | grep -v "SUCCESS!" | grep -v '\-\-' | grep -v "Building" | grep -v "  "
cp /c/'Program Files (x86)'/Steam/steamapps/common/'Black Reliquary'/localization/missing_strings.csv missing_strings.csv

echo ">> MISSING"
echo " "

cat missing_strings.csv | grep -v ",PSN," | grep -v ",switch," | grep -v ",xb1,"

echo " "
echo " "
echo ">> INVALID"
echo " "

grep -r ".*" review

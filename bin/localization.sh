# ./bin/localization.sh

echo " "
echo ">> CLEANING"
echo " "

(cd "/c/Program Files (x86)/Steam/steamapps/common/Black Reliquary/localization/";ls -l *.loc2;rm *.loc2) 2> /dev/null
rm review/*.xml
rm build/*.xml
echo "" > "/c/Program Files (x86)/Steam/steamapps/common/Black Reliquary/localization/missing_strings.csv"

echo " "
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
(cd "/c/Program Files (x86)/Steam/steamapps/common/Black Reliquary/localization/"; ls -l *.loc2)
cp /c/'Program Files (x86)'/Steam/steamapps/common/'Black Reliquary'/localization/missing_strings.csv missing_strings.csv 2> /dev/null

echo " "
echo " "
echo ">> MISSING"
echo " "

cat missing_strings.csv | grep -v ",switch," | grep -v ",xb1,"

echo " "
echo " "
echo ">> ANOMALY"
echo " "

grep -r ".*" review

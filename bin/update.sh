rm ./black_reliquary/*.xml 2> /dev/null
cp /c/'Program Files (x86)'/Steam/steamapps/common/'Black Reliquary'/localization/*.xml ./black_reliquary/
rm ./black_reliquary/PSN.string_table.xml
rm ./black_reliquary/switch.string_table.xml
rm ./black_reliquary/xb1.string_table.xml

rm ./compact/*.xml 2> /dev/null
cp ./black_reliquary/*.xml ./compact/

sed -i 's/<!--.*-->//g' ./compact/*.xml
sed -i 's@<root>@@g' ./compact/*.xml
sed -i 's@</root>@@g' ./compact/*.xml
sed -i 's@<language id="english">@@g' ./compact/*.xml
sed -i 's@</language>@@g' ./compact/*.xml
sed -i 's/<?xml version="1.0" encoding="UTF-8"?>//g' ./compact/*.xml

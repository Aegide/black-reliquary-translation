# ./bin/update.sh

# Gets black_reliquary files
rm ./black_reliquary/*.xml 2> /dev/null
cp /c/'Program Files (x86)'/Steam/steamapps/common/'Black Reliquary'/localization/*.xml ./black_reliquary/
rm ./black_reliquary/switch.string_table.xml
rm ./black_reliquary/xb1.string_table.xml

# Gets compact files
rm ./compact/*.xml 2> /dev/null
cp ./black_reliquary/*.xml ./compact/

# Removes comments
sed -i 's@<!--.*-->@@g' ./compact/*.xml

# Removes root tags
sed -i 's@<root>@@g' ./compact/*.xml
sed -i 's@</root>@@g' ./compact/*.xml

# Removes language tags
sed -i 's@<language id="english">@@g' ./compact/*.xml
sed -i 's@</language>@@g' ./compact/*.xml

# Removes xml tags
sed -i 's@<?xml version="1.0" encoding="UTF-8"?>@@g' ./compact/*.xml

# Removes characters before "<entry>"
sed -i 's@^.*<entry@<entry@g' ./compact/*.xml

# Removes useless line returns
sed -i -z 's@entry>[\n\t]*<entry@entry>\n<entry@g' ./compact/*.xml

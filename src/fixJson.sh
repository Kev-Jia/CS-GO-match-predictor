#!/bin/sh

OUTPUT="events.json"
attributes=("id:" "stars:" "date:" "team1:" "name:" "logo:" "team2:" "result:" "format:" "map:")

# fix JSON attributes
for i in ${attributes[@]}; do
    sed -i "s/$i/\"${i::-1}\":/g" $OUTPUT
done

# change all ' to "
sed -i "s/'/\"/g" $OUTPUT

# remove all [] brackets
sed -i "s/\[//g" $OUTPUT
sed -i "s/\]//g" $OUTPUT

# replace all } to },
# MANUAL INTERVENTION REQUIRED
# last }, of file will need to be manually changed to }
# i'm too lazy to find the proper regex for that
sed -i "s/}/},/g" $OUTPUT
sed -i "s/,,/,/g" $OUTPUT

# re-add [ at start of file and ] at end of file
# MANUAL INTERVENTION REQUIRED
# unnecessary newlines at start and end of file should be trimmed manually
sed -i "1 i\[" $OUTPUT
echo "" >> $OUTPUT
echo "]" >> $OUTPUT

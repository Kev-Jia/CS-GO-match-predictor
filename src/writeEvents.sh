#!/bin/sh

OUTPUT="matches.json"
eventIDs=(6343 6219 6136 6137 6384 6372 6138 6345 6510 6503 6140 6346 6141 6588 6586 6348 6349)

# clear output file for overwriting
echo "" > $OUTPUT

# write matches for each event
for i in ${eventIDs[@]}; do
    node fetchEvents.js $i >> $OUTPUT
    echo "" >> $OUTPUT
    echo "data for event $i written to $OUTPUT"
done

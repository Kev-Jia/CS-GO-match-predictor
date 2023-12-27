const {HLTV, BestOfFilter} = require('hltv');
const fs = require('fs');

const myHLTV = HLTV.createInstance({loadPage: (url) => fetch(url)});

let events2022 = 
[
    [6343, "BLAST Premier Spring Groups 2022"],
    [6219, "IEM Katowice 2022 Play-in"],
    [6136, "IEM Katowice 2022"],
    [6137, "ESL Pro League Season 15"],
    [6384, "PGL Antwerp Major 2022 Challengers Stage"],
    [6372, "PGL Antwerp Major 2022"],
    [6138, "IEM Dallas 2022"],
    [6345, "BLAST Premier Spring Finals 2022"],
    [6510, "Roobet Cup 2022"],
    [6503, "IEM Cologne 2022 Play-in"],
    [6140, "IEM Cologne 2022"],
    [6346, "BLAST Premier Fall Groups 2022"],
    [6141, "ESL Pro League Season 16"],
    [6588, "IEM Rio Major 2022 Challengers Stage"],
    [6586, "IEM Rio Major 2022"],
    [6348, "BLAST Premier Fall Finals 2022"],
    [6349, "BLAST Premier World Final 2022"]
];

/* let events2023 =
[
    [6970, "BLAST Premier Spring Groups 2023"],
    [6810, "IEM Katowice 2023 Play-in"],
    [6809, "IEM Katowice 2023"],
    [6862, "ESL Pro League Season 17"],
    [6864, "IEM Rio 2023"],
    [6794, "BLAST.tv Paris Major 2023 Challengers Stage"],
    [6793, "BLAST.tv Paris Major 2023"],
    [6861, "IEM Dallas 2023"],
    [6972, "BLAST Premier Spring Finals 2023"],
    [6973, "BLAST Premier Fall Groups 2023"],
    [6812, "IEM Cologne 2023 Play-in"],
    [6811, "IEM Cologne 2023"],
    [7128, "Gamers8 2023"]
]; */


// create list of only event IDs
let eventIDs = [];
for(let i in events2022)
{
    eventIDs.push(events2022[i][0]);
}

// process.argv.forEach((value, index) => {console.log(index, value); });

//[6343, 6219, 6136, 6137, 6384, 6372, 6138, 6345, 6510, 6503, 6140, 6346, 6141, 6588, 6586, 6348, 6349]
//let eventIDs2023 = [6970, 6810, 6809, 6862, 6864, 6794, 6793, 6861, 6972, 6973, 6812, 6811, 7128]



/* HLTV.getEventByName({name:"PGL Antwerp Major 2022 Challengers Stage"}).then((res) => {
    console.log(res)
}) */

/* HLTV.getEvent({id: 6140}).then(res => {
    console.log(res)
}) */

// clear file before writing data

// write data
// newline for each event
/* for(let i in eventIDs)
{
    console.log(eventIDs[i])
    HLTV.getResults({eventIds: eventIDs[i], bestOfX: BestOfFilter.BO3, delayBetweenPageRequests: 15000}).then(res => {
        fs.appendFile("eventData.txt", JSON.stringify(res), (err) => {if (err) throw err})
    });
    console.log("success") 
} */

HLTV.getResults({eventIds: process.argv[2], bestOfX: [BestOfFilter.BO3], delayBetweenPageRequests: 15000}).then(res => {
    console.log(res)
    // fs.appendFile("eventData.txt", JSON.stringify(res), (err) => {if (err) throw err})
});


// write EOL character
// fs.appendFile("eventData.txt", "\n", (err) => {if (err) throw err})
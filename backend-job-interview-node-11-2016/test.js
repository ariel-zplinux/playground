axios = require('axios');

const input = [];
const output = [];
var lastIndex = 0;
// to check and print each 2s
const DELAY = 2000;
// to work on 1000 entries
const SIZE = 1000;

// initialize arrays
for (var i=0; i<SIZE;i++) {
    input.push("http://www.google.com");
    output.push("5");
}

// store content of urls in global array 
storeUrls = (array, callback) => {
    array.map( (url, index) => {
        callback(url, index);
    })
}

// retrieve url content then store it
retrieveUrl = (url, index) => {
    axios.get(url)
    .then(function (response) {
        output[index] = response;
        console.log("success index: " +index);
    })
    .catch(function (error) {
        output[index] = error
        console.log("error index: "+index);
    });    
}

// print content, as much as possible, in original order, synchronously
printContentInOrder = () => {
    if (output[lastIndex] !== "5" && lastIndex < SIZE) {
        console.log("printing index: "+lastIndex);
        //console.log(output[lastIndex]);
        lastIndex++;
        printContentInOrder();
    }
    else if (lastIndex === SIZE) {
        console.timeEnd("Time elapsed");
        console.log("FINISHED");
        return ;
    }
    else {
        console.log("waiting lastIndex: "+lastIndex);
        setTimeout(printContentInOrder, DELAY);
    }
}

console.time("Time elapsed");
// call reading/storing operations
storeUrls(input, retrieveUrl);

// separate printing operations
setTimeout(printContentInOrder, DELAY);
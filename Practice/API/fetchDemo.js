/*

We'll primarily be using a RESTful style API for our project
for our case, that just means there will be a Base Url, parameters, and when we load that url, it
will return data in a format! this allows users to interact with our application, without directly
touching our db/code!  

with this api, we have control over what is, and how data is returned


as a practice, we'll be using the open-metro.com API to fetch weather data just to get a feel for it
for a demo, open the following link in your browser

https://api.open-meteo.com/v1/forecast?latitude=39.2555&longitude=-76.7113&hourly=temperature_2m

instead of a website, its JSON data! JSON is commonly used due to its native compatability w/ javascript

this is a "GET" request, just asking for data and waiting for a response 

like i mentioned, this url has a few components that inform the server of what to return:
Base Url: https://api.open-meteo.com/v1/forecast?  (note, the ? allows us to add data on top of the request, as anything following a ? is optional and just parsed by the server)


this API tells us to seperate parameters w/ an "&", and "=" if we want to assign a value to a parameter, so we can add parameters like this:
parameters:
latitude:   39.2555
longitude: -76.7113
hourly:    temperature_2m


we can also automate these http requests!
using javascript (as we will be handling requests application side, and therefore in browser)
we can use the "fetch" function! 

heres the basic documentation for the api 
https://open-meteo.com/en/docs#api_documentation

Base Url:
https://api.open-meteo.com/v1/forecast?
documentation lists various parameters that define whats returned


In javascript, we can use the "fetch" function to make a request to the API
because its an async function (meaning unsure when it will resolve timewise),
we use the a "promise" to say "hey, when this is done, do this"
promise:
.then()
.catch()

documentation:
https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise




syntax:
fetch(url)
.then(response => response.json())  // when the fetch is done, run the .json() function on it (parsing it into json)
.then(data => {
    // when we reach this point, the variable "data" is the result of the previous .then() (the parsed json)
    console.log("data: ", data);
    // heres where we actually interact with the data
})
.catch(error => {
    // not required, but we want to keep a stable system, so we gotta handle errors gracefully 
    console.error("error: ", error);
})



*/

const BASE_URL = "https://api.open-meteo.com/v1/forecast?";

function buildUrl(parameters){
    let url = BASE_URL;
    for(let key in parameters){
        url += `${key}=${parameters[key]}&`
    }
  console.log("built url: ", url);
    return url;
}

function fetchData(parameters){
    let url = buildUrl(parameters);
    fetch(url)
    .then(response => response.json())
    .then(data => {
        console.log("data: ", data);
    })
    .catch(error => {
        console.error("error: ", error);
    })
}


// passes parameters to the fetchData, builds the url, and does the fetch

fetchData({
    latitude: 39.2555,
    longitude: -76.7113,
    hourly: "temperature_2m"
})

// so, feel free to explore the documentation and try out different params to get a feel!


// however, what do we do with JSON data? how do we meaninfully interact with it?
// Javascript gives a few tools, that let us treat it like a Javascript Object:
//  so, dot/bracket notation, 
// see documentation
//  https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/JSON 

// so, based off that example return:
/*
{
  "latitude": 39.24907,
  "longitude": -76.70803,
  "generationtime_ms": 0.0585317611694336,
  "utc_offset_seconds": 0,
  "timezone": "GMT",
  "timezone_abbreviation": "GMT",
  "elevation": 61,
  "hourly_units": {
    "time": "iso8601",
    "temperature_2m": "°C"
  },
  "hourly": {
    "time": [
      "2026-02-13T00:00",
      "2026-02-13T01:00",
      "2026-02-13T02:00",
      "2026-02-19T19:00",
       ....
      "2026-02-19T20:00",
      "2026-02-19T21:00",
      "2026-02-19T22:00",
      "2026-02-19T23:00"
    ],
    "temperature_2m": [-0.3, -0.8, -0.6, -1.8, -2.2, -2.3, -2.5, -3.3, -2.6, -3.5, -3.8, -4.1, -4.6, -4.1, -2.4, -1.2, -0.1, 0.6, 1.2, 1.9, 1.9, 1.6, 1.3, -0.5, -1.2, -1.2, -1.2, -1.3, -1.4, -2.1, -2.5, -2.5, -1.8, -2.2, -2.4, -2.1, -1.7, -0.2, 3.4, 6.5, 8.4, 10.4, 11.8, 12.7, 13.3, 13.5, 12.3, 9, 7, 6.4, 5.5, 5.1, 4.3, 3.1, 2.7, 1.4, 0.6, 0.2, -0.2, -0.5, -0.5, 0.6, 2.5, 4.8, 6, 5.9, 5, 3.5, 3.3, 3.2, 2.7, 2.3, 2.1, 1.9, 1.8, 1.7, 1.7, 1.7, 1.7, 1.5, 1.4, 1.4, 1.4, 1.4, 1.3, 1.3, 1.4, 1.8, 2.6, 4.2, 5.4, 6.4, 7, 6.8, 6, 4.5, 3.6, 2.8, 2.2, 1.7, 1.3, 1, 0.7, 0.6, 0.5, 0.4, 0.4, 0.4, 0.4, 0.9, 2.5, 4.2, 6.1, 7.7, 9.3, 10.3, 11, 10.8, 9.4, 8.1, 7.7, 6.9, 6.9, 6.7, 6.5, 6.4, 6.4, 6.5, 6.4, 6.2, 6, 5.8, 5.5, 5.6, 5.9, 6.4, 7, 7.8, 8.5, 9, 9.5, 9.7, 9.5, 9.1, 8.7, 8.6, 8.6, 8.5, 8.3, 8, 7.8, 7.7, 7.6, 7.5, 6.9, 6.2, 6.3, 7.7, 9.8, 11.8, 13.5, 15.1, 16.4, 17.2, 17.7, 17.5, 16.1, 13.9]
  }
}
*/

// so, we can iterate the "temperature_2m" as an array natively, with a syntax like
// data (the base json object).hourly (key in json).temperature_2m (key in json, which is an array) (which is the array!)
// for(let temp of data.hourly.temperature_2m){
//    console.log(temp);
// }


// we'll define our own API and its returns, so this is jsut a more conceptual demo


// and of course, we'll use Javascript to interact with the DOM, letting us modify the webpage based on the data we get back from our API!
//
//
// final note: beyond GET requests, we will also use "POST", which lets us send data TO the server.
// well use this to handle check-in information and allow for tutors to update if they need to cancel or delay a session, etc
//
// see the ~/app.py for a look at the syntax of our Flask API, its pretty straightforward!

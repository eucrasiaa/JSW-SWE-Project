
// reading from local file ./TutorData.json
/*
Example
[
  {
    "Course": "BIOL 101",
    "Day": "Monday",
    "Start Time": "11:00",
    "End Time": "13:00",
    "Tutor": "Susanna"
  },
  {
    "Course": "BIOL 101",
    "Day": "Monday",
    "Start Time": "16:00",
    "End Time": "17:00",
    "Tutor": "Angela"
  },
  {
    "Course": "BIOL 101",
    "Day": "Tuesday",
    "Start Time": "12:00",
    "End Time": "14:00",
    "Tutor": "Shakib"
  },
  {
    "Course": "BIOL 101",
    "Day": "Tuesday",
    "Start Time": "13:00",
    "End Time": "16:00",
    "Tutor": "Zoya"
  },
  //   */
const fs = require('fs');
const path = require('path');

const jsdom = require('jsdom');
const { JSDOM } = require('jsdom');
function readJsonFile(filePath) {
  return new Promise((resolve, reject) => {
    fs.readFile(filePath, 'utf8', (err, data) => {
      if (err) {
        reject(err);
        return;
      }
      try {
        const jsonData = JSON.parse(data);
        resolve(jsonData);
      } catch (parseErr) {
        reject(parseErr);
      }
    });
  });
}
/*
<div class="sights-expander-wrapper mceNonEditable">
<div id="sights-expander-header-86994" class="sights-expander-trigger mceNonEditable" tabindex="0" role="button" aria-expanded="true" aria-controls="sights-expander-content-86994">
<div class="mceEditable">BIOL 101 – Concepts of Biology</div> READ THIS
</div>
<div id="sights-expander-content-86994" class="sights-expander-content mceNonEditable" role="region" aria-labelledby="sights-expander-header-86994">
<div class="mceEditable">
-- !! INSERT INTO HERE (not on page)
<p><strong>Tutors for BIOL 101 are available on the following days and times:</strong></p>

<p><strong>Monday</strong><br>
11:00 a.m. – 1:00 p.m. – Susanna<br>
4:00 p.m. – 5:00 p.m. – Angela</p>
<p><strong>Tuesday</strong><br>
Noon – 2:00 p.m. – Shakib<br>
1:00 p.m. – 4:00 p.m. – Zoya<br>
1:30 p.m. – 5:00 p.m. – Aren</p>
<p><strong>Wednesday</strong><br>
11:30 a.m. – 1:00 p.m. – Tristan<br>
1:00 p.m. – 2:00 p.m. – Lillian<br>
4:30 p.m. – 6:00 p.m. – Angela</p>
<p><strong>Thursday</strong><br>
12:30 p.m. – 2:00 p.m. – Shakib<br>
1:00 p.m. – 4:00 p.m. – Zoya<br>
1:00 p.m. – 4:00 p.m. – Avi</p>
<p><strong>Friday</strong><br>
11:00 a.m. – 1:00 p.m. – Aren</p>
</div>
</div>
</div>


*/

// https://raw.githubusercontent.com/eucrasiaa/JSW-SWE-Project/refs/heads/main/TutorData.json//

function fetchTutorsFromJson(url) {
  // return window.fetch(url)
  return fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
      }
      return response.json();
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
}

const tutorsUrl = 'https://raw.githubusercontent.com/eucrasiaa/JSW-SWE-Project/refs/heads/main/TutorData.json';
let TutorJson=null;
fetchTutorsFromJson(tutorsUrl)
  .then(tutors => {
    if (tutors) {
      TutorJson=tutors;
      insertTutorsIntoPage(tutors);
    }
  })
  .catch(error => {
    console.error('Error fetching tutors:', error);
  });

// mceEditable, either find parent and then .parentElement.parentElement.children[1].children[0]
// or. next index in list from class title one is the div...
//
function insertIDs(){
  //read in Drop_In_Admin.html
  //find all with class mceEditable, if text is format of [A-Z]{2,5} [0-9]{3} – (.+) 
  let elements = document.getElementsByClassName("mceEditable");
  for (let i = 0; i < elements.length; i++) {
    let text = elements[i].innerText;
    let match = text.match(/([A-Z]{2,5}) ([0-9]{3}) – (.+)/); //regex to match text format of dropdowns
    if (match) {
      let dept = match[1];
      let courseNum = match[2];
      let courseName = match[3];
      let id = dept + "_" + courseNum;
      console.log("regex-d: " + dept + " " + courseNum + " " + courseName);
      elements[i].parentElement.parentElement.children[1].children[0].id = id;
    }
  }
}

function validateIDs(){
  let elements = document.getElementsByClassName("mceEditable");
  for (let i = 0; i < elements.length; i++) {
    if(elements[i].id){
      console.log("id: " + elements[i].id);
      if(elements[i-1].innerText.includes(elements[i].id.split("_")[0]) && elements[i-1].innerText.includes(elements[i].id.split("_")[1])){
        console.log("validated: " + elements[i].id);
      } else {
        console.error("validation failed for: " + elements[i].id);
      }
    }
  }
}

function sortByClassAndDay(tutors){
  let sorted = {};
  tutors.forEach(tutor => {
    let course = tutor["Course"];
    let day = tutor["Day"];
    if (!sorted[course]) {
      sorted[course] = {};
    }
    if (!sorted[course][day]) {
      sorted[course][day] = [];
    }
    sorted[course][day].push(tutor);
  });
  console.log("sorted: " + JSON.stringify(sorted));
  return sorted;
}
/*
day section is:
<div class="BIOL_101">
  <p><strong>Monday</strong><br></p>
  <div class="BIOL_101_Monday">
    <p>11:00 a.m. – 1:00 p.m. – Susanna<p>
    <p>4:00 p.m. – 5:00 p.m. – Angela</p>
  </div>
</div>


*/
function insertTutorsIntoPage(tutors){
  let sortedTutors = sortByClassAndDay(tutors);
  for(let course in sortedTutors){
    for(let day in sortedTutors[course]){
      let daySection = document.createElement("div");
      daySection.className = course + "_" + day;
      dayHeader = document.createElement("p");
      dayHeader.innerHTML = "<strong>" + day + "</strong><br>";
      daySection.appendChild(dayHeader);
      sortedTutors[course][day].forEach(tutor => {
        daySection.appendChild(insertPGenerator(tutor));
      });
      let courseElem = document.getElementById(course.replace(" ", "_"));
      if(courseElem){
        courseElem.appendChild(daySection);
      } else {
        console.error("course element not found for: " + course);
      }
    }
  }
}

// function locateTutorSlot(course,day,time,tutor){
//   let elements = document.getElementsByClassName("mceEditable");
//   for (let i = 0; i < elements.length; i++) {
//     if(elements[i].id) { // if has id, its one of course elections. loop its children
//       for (let j = 0; j < elements[i].children.length; j++) {
//         if(elements[i].children[j].innerText.includes(day) && elements[i].children[j].innerText.includes(time) && elements[i].children[j].innerText.includes(tutor)){
//           console.log("found: " + course + " " + day + " " + time + " " + tutor);
//           // can it return a reference to elem?
//           return elements[i].children[j];
//         }
//       }
//     }
//   }
//   console.error("not found: " + course + " " + day + " " + time + " " + tutor);
//   return null;
//  }
//
// function demoLocate(){
//   let tutorSlot = locateTutorSlot("BIOL 101", "Thursday", "1:00 p.m. – 4:00 p.m.", "Avi");
//   if(tutorSlot){
//     tutorSlot.style.backgroundColor = "yellow";
//   }
// }

// updated using the classes!
// "BIOL 101" "Thursday" "13:00" "Zoya" 
function locateTutorSlot(course,day,time,tutor){
  let elements = document.getElementsByClassName(course + "_" + day);
  for (let i = 0; i < elements.length; i++) {
    if(elements[i].innerText.includes(time) && elements[i].innerText.includes(tutor)){
      // iterate thru children to find exact p with time and tutor
      for (let j = 0; j < elements[i].children.length; j++) {
        if(elements[i].children[j].innerText.includes(time) && elements[i].children[j].innerText.includes(tutor)){
          console.log("found: " + course + " " + day + " " + time + " " + tutor);
          // can it return a reference to elem?
          return elements[i].children[j];
        }
      }
    }
  }
  console.error("not found: " + course + " " + day + " " + time + " " + tutor);
  return null;
}

function demoLocate(){
  let tutorSlot = locateTutorSlot("BIOL 101", "Thursday", "13:00", "Avi");
  if(tutorSlot){
    tutorSlot.style.backgroundColor = "yellow";
  }
}
demoLocate();

/*
 <div id="sights-expander-content-86994" class="sights-expander-content sights-expander-hidden mceNonEditable" role="region" aria-labelledby="sights-expander-header-86994">
<div class="mceEditable" id="BIOL_101">
<p><strong>Tutors for BIOL 101 are available on the following days and times:</strong></p>
<div class="BIOL 101_Monday"><p><strong>Monday</strong><br></p><p>11:00 – 13:00 – Susanna<br></p><p>16:00 – 17:00 – Angela<br></p></div><div class="BIOL 101_Tuesday"><p><strong>Tuesday</strong><br></p><p>12:00 – 14:00 – Shakib<br></p><p>13:00 – 16:00 – Zoya<br></p><p>13:30 – 17:00 – Aren<br></p></div><div class="BIOL 101_Wednesday"><p><strong>Wednesday</strong><br></p><p>11:30 – 13:00 – Tristan<br></p><p>13:00 – 14:00 – Lillian<br></p><p>16:30 – 17:00 – Angela<br></p></div><div class="BIOL 101_Thursday"><p><strong>Thursday</strong><br></p><p>12:30 – 14:00 – Shakib<br></p><p>13:00 – 16:00 – Zoya<br></p><p>13:00 – 16:00 – Avi<br></p></div><div class="BIOL 101_Friday"><p><strong>Friday</strong><br></p><p>11:00 – 13:00 – Aren<br></p></div></div>
</div>


*/
function isTimeInRange(current, start, end) {
  const [currentHour, currentMinute] = current.split(':').map(Number);
  const [startHour, startMinute] = start.split(':').map(Number);
  const [endHour, endMinute] = end.split(':').map(Number);

  const currentTotal = currentHour * 60 + currentMinute;
  const startTotal = startHour * 60 + startMinute;
  const endTotal = endHour * 60 + endMinute;

  // window starts 60 mins before 'start'
  const windowStart = startTotal - 60; 

  // highlight if: 
  // 1. we are within the 1-hour pre-start buffer or already started
  // 2. and we have not yet passed the end time
  return currentTotal >= windowStart && currentTotal <= endTotal;
}
function findAllOngoingSlots(){
  // parsing to find slots within the range of (-1 hour, +1 hour) of current time, and highlight them. BUT 
  let now = new Date();
  let dayOfWeek = now.toLocaleString('en-US', { weekday: 'long' });
  let currentTime = now.getHours() + ":" + now.getMinutes();
  console.log("current time: " + currentTime);
  let elements = document.getElementsByClassName("mceEditable");
  for (let i = 0; i < elements.length; i++) { // loop thru courses
    if(elements[i].id){ // if has id, its one of course elections. loop its children
      for (let j = 0; j < elements[i].children.length; j++) { // loop thru days
        if (elements[i].children[j].innerText.includes(dayOfWeek)){ // if day matches, loop thru slots
          for (let k = 0; k < elements[i].children[j].children.length; k++) { // loop thru slots
            let slotText = elements[i].children[j].children[k].innerText;
            let timeMatch = slotText.match(/([0-9]{1,2}:[0-9]{2})/g);
            if(timeMatch && timeMatch.length >= 2){
              let startTime = timeMatch[0];
              let endTime = timeMatch[1];
              if(isTimeInRange(currentTime, startTime, endTime)){
                console.log("ongoing slot: " + slotText);
                elements[i].children[j].children[k].style.backgroundColor = "lightgreen";
              }
            }
          }
        }
      }
    }
  }
} 
function insertPGenerator(tutorElem){
  let p = document.createElement("p");
  p.innerHTML = tutorElem["Start Time"] + " – " + tutorElem["End Time"] + " – " + tutorElem["Tutor"] + "<br>";
  return p;
}




function insertRenderIds(domdoc) {
  // Use querySelectorAll for better reliability in JSDOM
  let elements = domdoc.getElementsByClassName("mceEditable");
  for (let i = 0; i < elements.length; i++) {
    // JSDOM often prefers textContent over innerText
    let text = elements[i].textContent.trim();
    let match = text.match(/([A-Z]{2,5}) ([0-9]{3}) – (.+)/);

    if (match) {
      let dept = match[1];
      let courseNum = match[2];
      let id = dept + "_" + courseNum;

      // Ensure the nested elements exist before assigning ID
      const target = elements[i].parentElement?.parentElement?.children[1]?.children[0];
      if (target) {
        target.id = id;
        console.log(`Inserted ID: ${id}`);
      }
    }
  }
}

function insertIDsIntoFile() {
  fs.readFile('./Drop_In_Admin.html', 'utf8', (err, data) => {
    if (err) return console.error(err);

    const dom = new JSDOM(data);
    const doc = dom.window.document;

    insertRenderIds(doc);

    // Use dom.serialize() instead of XMLSerializer for standard HTML
    const newData = dom.serialize();

    fs.writeFile('./Drop_In_Admin_IDS.html', newData, 'utf8', (err) => {
      if (err) return console.error(err);
      console.log('File saved successfully!');
    });
  });
}
//
// function deleteAllSections(domdoc){
//   // for every div with class ="mceEditable" and an id, delete every child thats not the first one ()
//   let elements = domdoc.getElementsByClassName("mceEditable");
//   for (let i = 0; i < elements.length; i++) {
//     if(elements[i].id){
//       while(elements[i].children.length > 1){
//         elements[i].removeChild(elements[i].lastChild);
//       }
//     }
//   }
// }
// function deleteSectionsInFile() {
//   fs.readFile('./Drop_In_Admin_IDS.html', 'utf8', (err, data) => {
//     if (err) return console.error(err);
//
//     const dom = new JSDOM(data);
//     const doc = dom.window.document;
//
//     deleteAllSections(doc);
//
//     const newData = dom.serialize();
//
//     fs.writeFile('./Drop_In_Admin_CLEAN.html', newData, 'utf8', (err) => {
//       if (err) return console.error(err);
//       console.log('File cleaned successfully!');
//     });
//   });
// }
// deleteSectionsInFile();

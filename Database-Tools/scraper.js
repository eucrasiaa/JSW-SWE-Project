(() => {
  const tutorData = {};

  const formatTime = (timeStr, period) => {
    let [hours, minutes] = timeStr.split(':').map(Number);
    period = period.toLowerCase().replace(/\./g, ''); 
    if (period === 'pm' && hours < 12) hours += 12;
    if (period === 'am' && hours === 12) hours = 0;

    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
  };

  const wrappers = document.querySelectorAll('.sights-expander-wrapper');

  wrappers.forEach(wrapper => {
    const headerText = wrapper.querySelector('.sights-expander-trigger .mceEditable')?.innerText || "";
    const courseCode = headerText.split('–')[0].trim();

    const content = wrapper.querySelector('.sights-expander-content .mceEditable');
    if (!content) return;

    let currentDay = "";
    const lines = content.innerText.split('\n').map(l => l.trim()).filter(l => l.length > 0);

    const daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

    lines.forEach(line => {
      if (daysOfWeek.some(day => line.includes(day))) {
        currentDay = daysOfWeek.find(day => line.includes(day));
        return;
      }
      const timeRegex = /(\d{1,2}:\d{2})\s*([ap]\.m\.)\s*[–-]\s*(\d{1,2}:\d{2})\s*([ap]\.m\.)\s*[–-]\s*(.*)/i;
      const match = line.match(timeRegex);

      if (match && currentDay) {
        const startTime = formatTime(match[1], match[2]);
        const endTime = formatTime(match[3], match[4]);
        const tutorName = match[5].trim();
        if (!tutorData[tutorName]) {
          tutorData[tutorName] = { Tutor: tutorName, Schedule: [] };
        }
        const existingEntry = tutorData[tutorName].Schedule.find(s => 
          s.Day === currentDay && s.StartTime === startTime && s.EndTime === endTime
        );
        if (existingEntry) {
          if (!existingEntry.Courses.includes(courseCode)) {
            existingEntry.Courses.push(courseCode);
          }
        } else {
          tutorData[tutorName].Schedule.push({
            Day: currentDay,
            StartTime: startTime,
            EndTime: endTime,
            Courses: [courseCode]
          });
        }
      }
    });
  });

  const finalJson = Object.values(tutorData);
  const blob = new Blob([JSON.stringify(finalJson, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'tutor_schedules.json';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  console.log("Parsing complete. File downloaded.", finalJson);
})();


let a = document.getElementsByClassName("sights-expander-trigger mceNonEditable")
let ave = ""
for (el of a){
    ave+=el.innerText+"\n"
}


const regex = /^(?<Dept>[A-Z]+)\s*[–-]?\s*(?<CourseNumber>\d+)\s*[–-]?\s*(?<LongTitle>.*)$/gm;

const parsedData = [];
let match;

while ((match = regex.exec(ave)) !== null) {
  parsedData.push(match.groups);
}
const jsonOutput = JSON.stringify(parsedData, null, 2);

console.log(jsonOutput);



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

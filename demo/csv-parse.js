// reading from local file ./TutorData.csv
/*
Example
Course,Day,Start Time,End Time,Tutor  
BIOL 101,Monday,11:00,13:00,Susanna  
BIOL 101,Monday,16:00,17:00,Angela  
BIOL 101,Tuesday,12:00,14:00,Shakib  
BIOL 101,Tuesday,13:00,16:00,Zoya  
BIOL 101,Tuesday,13:30,17:00,Aren  
BIOL 101,Wednesday,11:30,13:00,Tristan  
BIOL 101,Wednesday,13:00,14:00,Lillian  
BIOL 101,Wednesday,16:30,17:00,Angela  
BIOL 101,Thursday,12:30,14:00,Shakib  
BIOL 101,Thursday,13:00,16:00,Zoya  
BIOL 101,Thursday,13:00,16:00,Avi  
BIOL 101,Friday,11:00,13:00,Aren  
BIOL 140,Monday,11:00,13:00,Susanna  
BIOL 140,Monday,16:00,17:00,Angela  
BIOL 140,Tuesday,12:00,14:00,Shakib  




*/
const fs = require('fs');

fs.readFile('./TutorData.csv', 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading the file:', err);
    return;
  }
  // we are formatting to embed into a website, so we are converting the csv data into a json format
  const lines = data.split('\n');
  const headers = lines[0].split(',').map(header => header.trim());
  const tutors = lines.slice(1).map(line => {
    const values = line.split(',').map(value => value.trim());
    return headers.reduce((obj, header, index) => {
      obj[header] = values[index];
      return obj;
    }, {});
  });
  console.log(JSON.stringify(tutors, null, 2));
  // write to file
  fs.writeFile('./TutorData.json', JSON.stringify(tutors, null, 2), 'utf8', (err) => {
    if (err) {
      console.error('Error writing the file:', err);
      return;
    }
    console.log('File has been written successfully.');
  });
});

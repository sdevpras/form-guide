
const loadJSONFile = () => {
    let input, fr;
    const receivedText = (e) => {
        let lines = e.target.result;
        return JSON.parse(lines);
    }
    if (typeof window.FileReader !== 'function') {
      alert("The file API isn't supported on this browser yet.");
      return;
    }
    input = document.getElementById('fileinput');
    if (!input) {
      alert("Couldn't find the Fileinput element.");
    }
    else if (!input.files) {
      alert("This browser doesn't seem to support the `files` property of file inputs.");
    }
    else if (!input.files[0]) {
      alert("Please select a file before clicking 'Load'");
    }
    else {
      file = input.files[0];
      fr = new FileReader();
      fr.onload = receivedText;
     // fr.readAsText(file);
    }
    
};
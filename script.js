let currentTable = '';

const loadJSONFile = () => {
  let input, fr;
  const receivedText = (e) => {
      let lines = e.target.result;
      let data = JSON.parse(lines);
      console.log(data);
      createElements(data);
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
    fr.readAsText(file);
  }
};

const createElements = (data) => {
  let root = document.getElementById('root');
  let div = document.createElement('div');
  div.setAttribute('id', 'tableDiv')
  let select = createSelectTag('leagues', data);
  select += createAllTables(data);
  div.innerHTML = select;
  root.appendChild(div);
}

const createSelectTag = (id, data) => {
  let options = '';
  options += `<option disabled selected value> -- Select League -- </option>`;
  for (option of Object.keys(data)){
    options += `<option value='${option}'>${option}</option>`;
  }
  let select = `<select id=${id} onchange="replaceTable(this)">` + options + `</select>`;
  return select;
};

const replaceTable = (selectElement) => {
  let tables = document.getElementsByTagName('table');
  for (table of tables){
    table.hidden = true;
  }
  document.getElementById(selectElement.value).hidden = false;
  currentTable = selectElement.value;
}

const createAllTables = (data) => {
  let tableHtml = '';
  for (id of Object.keys(data)){
    tableHtml += createTable(id, data);
  }
  return tableHtml;
};

const createTable = (id, data) => {
  let tableData = data[id];
  let table = `<table id='${id}' hidden><thead><tr>
  <th onclick='sortTable(0)'>Rank</th>
  <th onclick='sortTable(1, true)'>Team</th>
  <th onclick='sortTable(2)'>P</th>
  <th onclick='sortTable(3)'>W</th>
  <th onclick='sortTable(4)'>D</th>
  <th onclick='sortTable(5)'>L</th>
  <th onclick='sortTable(6)'>F</th>
  <th onclick='sortTable(7)'>A</th>
  <th onclick='sortTable(8)'>GD</th>
  <th onclick='sortTable(9)'>Pts</th>
  <th onclick='sortTableByForm()'>Form</th>
  <th hidden>Formlast</th>
  </tr></thead><tbody>`;
  for (row of tableData){
    table += `<tr>
      <td>${row['rank']}</td>
      <td>${row['team']}</td>
      <td>${row['played']}</td>
      <td>${row['won']}</td>
      <td>${row['drawn']}</td>
      <td>${row['lost']}</td>
      <td>${row['for']}</td>
      <td>${row['against']}</td>
      <td>${row['gd']}</td>
      <td>${row['points']}</td>
      <td>${row['form']['formString']}</td>
      <td hidden>${row['form']['formLastSixPoints']}</td>
    </tr>`
  }
  table += `</tbody></table>`;
  return table;
}

const sortTable = (column, alphabetical = false) => {
  let table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById(currentTable);
  switching = true;
  dir = "asc"; 
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("TD")[column];
      y = rows[i + 1].getElementsByTagName("TD")[column];
      if (dir == "asc") {
        if ((alphabetical === true && x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) || (alphabetical === false && Number(x.innerHTML) > Number(y.innerHTML))) {
          shouldSwitch= true;
          break;
        }
      } else if (dir == "desc") {
        if ((alphabetical === true && x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) || (alphabetical === false && Number(x.innerHTML) < Number(y.innerHTML))) {
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      switchcount ++;      
    } else {
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
};

const sortTableByForm = () => {
  let table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById(currentTable);
  switching = true;
  dir = "asc"; 
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName('TD')[11].innerHTML.split(',').map(Number);
      y = rows[i + 1].getElementsByTagName('TD')[11].innerHTML.split(',').map(Number);
      shouldSwitch = compareLists(dir, x, y);
      if(shouldSwitch === true) {
        break;
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      switchcount ++;      
    } else {
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
};

const compareLists = (dir, list1, list2) => {
  if (dir == 'asc') {
    for (j = 0; j < list1.length; j++) {
      if(list1[j] > list2[j]) {
        return true;
      } else if (list1[j] === list2[j]) {
        continue;
      } else {
        return false;
      }
    }
  } else {
    for (j = 0; j < list1.length; j++) {
      if(list1[j] < list2[j]) {
        return true;
      } else if (list1[j] === list2[j]) {
        continue;
      } else {
        return false;
      }
    }
  }
};
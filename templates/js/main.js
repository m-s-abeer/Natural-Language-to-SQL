let fileList = [];
let printConsole = (msg) =>{
  $("#console_output").html($("#console_output").html() + msg + '\n');
  $("#console_output").animate({ scrollTop: $('#console_output').prop("scrollHeight")}, 1000);
}

let printDataList = (data) => {
  console.log('printing data');
  console.log(data);
  $('#fetchedData').html('');
  data.forEach(element => {
    $('#fetchedData').append('<li>'+element+'</li>');
  });
}

let submitNlq = () =>{
  $.ajax({
    url: '/query',
    method: 'POST',
    dataType: 'JSON',
    data: {'query': $("#nlq").val()},
    success: (msg) => {
      console.log('Query Returned!');
      // console.log(msg);
      // console.log(msg.data);
      // console.log(typeof msg);
      // console.log(msg.data.length);
      // console.log('data type: ');
      // console.log(typeof msg.data)
      printConsole(msg.nlq);
      // printConsole(JSON.stringify(msg.hash));
      printConsole(msg.sql)
      $('#abeerSql').val(msg.abeerSql);
      // printDataList(msg.data);
      // printConsole(JSON.stringify(msg.dependencies));
      // printConsole(JSON.stringify(msg.parserdepend));
      // printConsole(JSON.stringify(msg.data));
      printConsole(JSON.stringify(msg.time));
    }
  });
}

let getFileList = () =>{
  $.ajax({
    url: '/filelist',
    method: 'GET',
    success: (data) => {
      fileList = data;
      generateFileList(data);
      printConsole('File List Fetched');
    }
  });
}

let generateFileList = (list) => {
  $("#file-list").html("");
  for (let i = 0; i < list.length; i++){
    $('<tr><td>'+list[i]+'</td><td><button class="btn btn-primary" onclick="fileChoose('+i+')">Choose</button></td></tr>').appendTo("#file-list");
  }
}

let fileChoose = (n) => {
  let path = 'uploads/' + fileList[n];
  console.log(path);
  $.ajax({
    url: '/filechange',
    method: 'POST',
    data: {'file': path},
    success: (msg) =>{
      console.log(msg);
      printConsole(msg);
      fetchMeta();
      showcurrentfile(path);
      printConsole('File Changed');
    }
  })
}

let upload = () =>{
  let data = new FormData();
  data.append('file', $("#file_input")[0].files[0]);
  $.ajax({
    url: '/upload',
    method: 'POST',
    data: data,
    cache: false,
    processData: false,
    contentType: false,
    error: () => {
      console.log("Upload Error.");
      printConsole("Upload Error");
    },
    success: (data) =>{
      console.log(data);
      printConsole("Upload Successful");
      showcurrentfile(data.path);
      fetchMeta();
    }
  });
}

let showcurrentfile = (path) =>{
  $("#uploadform")[0].style.display = "none";
  $("#upload_div").html("<h4>Currently Selected: " + path + "</h4>");
}


let fetchMeta = () => {
    $.ajax({
        url: '/getmeta',
        method: 'GET',
        dataType: 'json',
        success: (msg) => {
            console.log(msg);
            jsonPrettyHighlightToId(msg, 'json_print');
            printConsole('loaded metadata');
        }
    });
}

function jsonPrettyHighlightToId(jsonobj, id_to_send_to) {

    var json = JSON.stringify(jsonobj, undefined, 2);

    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    json = json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'color: darkorange;';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'color: red;';
            } else {
                cls = 'color: green;';
            }
        } else if (/true|false/.test(match)) {
            cls = 'color: blue;';
        } else if (/null/.test(match)) {
            cls = 'color: magenta;';
        }
        return '<span style="' + cls + '">' + match + '</span>';
    });
    document.getElementById(id_to_send_to).innerHTML = json;
}

let startup = () => {
  getFileList();
}

window.onload = startup;

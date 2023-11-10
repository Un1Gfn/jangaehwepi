// https://datatables.net/manual/ajax
// https://datatables.net/examples/ajax/null_data_source.html

// ajax parameters, inherited from jquery to datatables
// https://api.jquery.com/jQuery.ajax/

// https://datatables.net/reference/option/dom
// https://datatables.net/extensions/buttons/

API = "http://192.168.0.223:6081";

$(document).ready(function(){

  function req(u){
    let request = new XMLHttpRequest();
    request.open("GET", u, async=false);
    request.send(null);
    return request.responseText;
  }

  // let id = document.getElementById.bind(document);
  function id(i){
    return document.getElementById(i);
  }

  // active node
  let j = JSON.parse(req(`${API}/g_list`));
  id("id_active").value = `active = ${j.active}`;

  // deactivate button
  id("id_deactivate").onclick = function(){
    req(`${API}/g_deactivate`);
    location.reload(true);
  };

  id("id_update").onclick = function(){
    req(`${API}/g_update`);
    location.reload(true);
  };

  // render table
  let table = new DataTable('#id_table', {
    info: true,
    ordering: true,
    paging: false,
    dom: 'Bf',
    data: j.nodes,
    columns: [
      { data: 0,    width: "1em",  type: "num", },
      { data: 1,    width: "5em",  type: "num", },
      { data: 2,    width: "auto" },
      { data: null, width: "2em",  defaultContent: "<button class='c_rowbutton'>&nbsp;</button>", orderable: false },
      { data: null, width: "2em",  defaultContent: "<button class='c_rowbutton'>&nbsp;</button>", orderable: false }
    ]
  });

  // activate button
  table.on('click', 'button', function(e){
    req(`${API}/g_deactivate`);
    let data = table.row(e.target.closest('tr')).data();
    req(`${API}/g_activate/${data[0]}`);
    location.reload(true);
  });

})

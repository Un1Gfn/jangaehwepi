// https://datatables.net/manual/ajax
// https://datatables.net/examples/ajax/null_data_source.html

// ajax parameters, inherited from jquery to datatables
// https://api.jquery.com/jQuery.ajax/

// https://datatables.net/reference/option/dom
// https://datatables.net/extensions/buttons/

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
  j = JSON.parse(req(`${API}/g_pull/`));
  id("id_active").value = `active = ${j.active}`;

  // deactivate button
  id("id_deactivate").onclick = function(){
    req(`${API}/g_deactivate/`);
    location.reload(true);
  };

  // benchmark button
  id("id_benchmark").onclick = function(){
    req(`${API}/g_benchmark/`);
  };

  // yaml download url
  id("id_yaml").href = SUBSCRIPTION;

  id("id_update").onclick = function(){

    let f = new FormData();
    f.append("fd_file", id("id_file").files[0]);

    let request = new XMLHttpRequest();
    request.open("POST", `${API}/g_upload/`, async=false);
    request.send(f);
    location.reload(true);
  };

  // render table
  let table1 = new DataTable('#id_table1', {
    info: true,
    ordering: true,
    paging: false,
    dom: 'Bf',
    data: j.list1,
    columns: [
      { data: 0,    width: "1em",  type: "num", },
      { data: 2,    width: "5em",  type: "num", },
      { data: 1,    width: "auto" },
      { data: null, width: "2em",  defaultContent: "<button class='c_activate'>&nbsp;</button>", orderable: false },
      { data: null, width: "2em",  defaultContent: "<button class='c_blacklist'>&nbsp;</button>", orderable: false }
    ]
  });

  // activate button
  table1.on('click', 'button', function(e){
    let data = table1.row(e.target.closest('tr')).data();
    switch($(this).attr('class')){
      case "c_blacklist":
        req(`${API}/g_ban/${data[0]}`);
        location.reload(true);
        break;
      case "c_activate":
        req(`${API}/g_activate/${data[0]}`);
        location.reload(true);
        break;
      default:
        alert("err lt4tf5")
        break;
    }
  });

  let table2 = new DataTable('#id_table2', {
    info: false,
    ordering: false,
    paging: false,
    dom: '',
    data: j.list2,
    columns: [
      { data: 0,    width: "1em",  type: "num", },
      { data: null, width: "2em",  defaultContent: "<button class='c_allow'>&nbsp;</button>", orderable: false },
      { data: 1,    width: "auto" },
    ]
  });

  table2.on('click', 'button', function(e){
    let data = table2.row(e.target.closest('tr')).data();
    req(`${API}/g_allow/${data[0]}`);
    location.reload(true);
  });

})

// https://datatables.net/manual/ajax
// https://datatables.net/examples/ajax/null_data_source.html

// ajax parameters, inherited from jquery to datatables
// https://api.jquery.com/jQuery.ajax/

// https://datatables.net/reference/option/dom
// https://datatables.net/extensions/buttons/

API = "http://192.168.0.223:6081";

$(document).ready(function(){

  var table = new DataTable('#tb_nodes', {
    info: true,
    ordering: true,
    paging: false,
    dom: 'Bf',
    ajax: {
      url: API + "/g_list",
      dataSrc: "nodes",
      cache: false, // "_={timestamp}" in GET
    },
    columns: [
      { data: 0,    width: "1em",  type: "num", },
      { data: 1,    width: "5em",  type: "num", },
      { data: 2,    width: "auto" },
      { data: null, width: "5em",  defaultContent: "<button>ACTIVATE</button>", orderable: false }
    ],
    buttons: [
      {
        text: 'DEACTIVATE',
        action: function(e, dt, node, config){
          console.log(`${API}/g_deactivate`);
          $.get(`${API}/g_deactivate`, function(data) {
            console.log(data);
          });
        }
      }
    ]
  });

  table.on('click', 'button', function(e){
    let data = table.row(e.target.closest('tr')).data();
    console.log(`${API}/g_activate/${data[0]}`);
    $.get(`${API}/g_activate/${data[0]}`, function(data) {
      console.log(data);
    });
  });

})

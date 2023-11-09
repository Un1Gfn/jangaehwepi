// https://datatables.net/manual/ajax
// https://datatables.net/examples/ajax/null_data_source.html

// ajax parameters, inherited from jquery to datatables
// https://api.jquery.com/jQuery.ajax/

API = "http://192.168.0.223:6081"

var table = new DataTable('#tb_nodes', {
  info: true,
  ordering: true,
  paging: false,
  ajax: {
    url: API + "/list",
    dataSrc: "nodes",
    cache: false, // "_={timestamp}" in GET
  },
  "columns": [
    { data: 0,    width: "1em",  type: "num", },
    { data: 1,    width: "5em",  type: "num", },
    { data: 2,    width: "auto" },
    { data: null, width: "5em",  defaultContent: "<button>ACTIVATE</button>", orderable: false }
  ]
});

table.on('click', 'button', function (e) {
  let data = table.row(e.target.closest('tr')).data();
  alert("I = " + data[0]);
});

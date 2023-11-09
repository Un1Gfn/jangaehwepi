// https://datatables.net/manual/ajax
// https://datatables.net/examples/ajax/null_data_source.html

var table = new DataTable('#tb_nodes', {
  info: true,
  ordering: true,
  paging: false,
  "columns": [
    { width: "1em",  type: "num", },
    { width: "5em",  type: "num", },
    { width: "auto", type: "string" },
    { width: "5em", data: null, defaultContent: "<button>ACTIVATE</button>", orderable: false }
  ]
});

table.on('click', 'button', function (e) {
  let data = table.row(e.target.closest('tr')).data();
  alert("I = " + data[0]);
});

// columnDefs: [
//   { targets: [0, 2] , type: "num" },
//   { targets: 3,       data: null, defaultContent: '<button>activate</button>' },
//   { targets: 1,       type: "string" }
// ]

var table = new DataTable('#tb_nodes', {
  // "columns": [
  //   ...
  // ]
  columnDefs: [
    { targets: [0, 2] , type: "num" },
    { targets: 3,       data: null, defaultContent: '<button>activate</button>' },
    { targets: 1,       type: "string" }
  ]
})

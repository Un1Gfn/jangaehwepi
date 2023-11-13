var table = new DataTable('#tb_nodes', {
  ajax: {
    url: API + "/g_list",
    dataSrc: "nodes",
    cache: false, // "_={timestamp}" in GET
  },
  columnDefs: [
    { targets: [0, 2] , type: "num" },
    { targets: 3,       data: null, defaultContent: '<button>activate</button>' },
    { targets: 1,       type: "string" }
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
})

$.get(`${API}/g_activate/${data[0]}`, reload);

// hang, choose file button unresponsive
let now = new Date().getTime();
while(new Date().getTime() < now + 3000){;}



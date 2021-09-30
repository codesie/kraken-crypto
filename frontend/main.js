test = () => {
  const columnDefs = [
    { field: 'ordertxid' },
    { field: 'postxid' },
    { field: 'pair', rowGroup: true, hide: true },
    { field: 'time' },
    { field: 'type', rowGroup: true, hide: true },
    { field: 'ordertype' },
    {
      field: 'price',
    },
    { field: 'cost', aggFunc: 'sum' },
    { field: 'fee', aggFunc: 'sum' },
    { field: 'vol', aggFunc: 'sum' },
    { field: 'margin' },
    { field: 'misc' },
  ]

  // let the grid know which columns to use
  const gridOptions = {
    columnDefs: columnDefs,
    groupDisplayType: 'groupRows',
    animateRows: true,
    enableValue: true,
  }

  const gridDiv = document.querySelector('#myGrid')
  new agGrid.Grid(gridDiv, gridOptions)
  // fetch the row data to use and one ready provide it to the Grid via the Grid API
  agGrid
    .simpleHttpRequest({
      url: 'http://127.0.0.1:8000/api/trades',
    })
    .then((data) => {
      let rowData = []
      Object.values(data).forEach((value) => {
        rowData.push(value)
      })
      gridOptions.api.setRowData(rowData)
    })
}

let overview = {
  createTable: function () {
    const columnDefs = [
      { field: 'pair' },
      { field: 'volumeBuy' },
      { field: 'volumeSell' },
    ]

    // let the grid know which columns to use
    const gridOptions = {
      columnDefs: columnDefs,
      animateRows: true,
    }

    const gridDiv = document.querySelector('#myGrid')
    new agGrid.Grid(gridDiv, gridOptions)
    // fetch the row data to use and one ready provide it to the Grid via the Grid API
    agGrid
      .simpleHttpRequest({
        url: 'http://127.0.0.1:8000/api/trades/overview',
      })
      .then((data) => {
        console.log(data)
        gridOptions.api.setRowData(data)
      })
  },
}

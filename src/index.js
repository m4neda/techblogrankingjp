new gridjs.Grid({
  columns: [
    {
      name:'順位',
      formatter: (cell) => {
        return gridjs.html(`<b>${cell}</b>`)}
    },
    {
      name:'企業名',
      formatter: (cell, row) => {
        return gridjs.html(`<a href=${row.cells[5].data}>${cell}</a>`)}
    },
    'スコア',
    '記事数',
    'ブクマ数中央値',
    {
      name:'url',
      hidden: true
    }
  ],
  sort: true,
  search:true,
  pagination: true,
  server: {
    url: 'http://localhost:8080/',
    then: data => data.map(result => [result.rank, result.company_name, result.score,result.article_count, result.hatebu_count, result.url])
  }
}).render(document.getElementById("wrapper"));
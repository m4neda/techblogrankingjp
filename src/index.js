new gridjs.Grid({
  columns: [
    {
      name:'rank',
      formatter: (cell) => {
        return gridjs.html(`<b>${cell}</b>`)}
    },
    {
      name:'company_name',
      formatter: (cell, row) => {
        return gridjs.html(`<a href=${row.cells[4].data}>${cell}</a>`)}
    },
    'article_count',
    'hatebu_count',
    'Score',
    {
      name:'url',
      hidden: true
    }
  ],
  sort: true,
  pagination: {
    limit: 10
  },
  server: {
    url: 'http://localhost:8080/',
    then: data => data.map(result => [result.rank, result.company_name, result.article_count, result.hatebu_count, result.score, result.url])
  }
}).render(document.getElementById("wrapper"));
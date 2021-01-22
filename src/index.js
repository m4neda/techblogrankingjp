new gridjs.Grid({
  columns: ['company_name', 'hatebu_count', 'url'],
  pagination: {
    limit: 20
  },
  server: {
    url: 'https://s3-ap-northeast-1.amazonaws.com/m4neda.example.com/hatebucount.json',
    then: data => data.map(result => [result.company_name, result.hatebu_count, result.url])
  } 
}).render(document.getElementById("wrapper"));
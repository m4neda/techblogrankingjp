/* global gridjs */

new gridjs.Grid({
  columns: [
    {
      name: '順位',
      formatter: (cell) => {
        return gridjs.html(`<b>${cell}</b>`)
      }
    },
    {
      name: '企業名',
      formatter: (cell, row) => {
        return gridjs.html(`<a href=https://b.hatena.ne.jp/entrylist?url=${row.cells[5].data}>${cell}</a>`)
      }
    },
    'スコア',
    '記事数',
    'ブクマ数中央値',
    {
      name: 'url',
      hidden: true
    }
  ],
  sort: true,
  search: true,
  pagination: true,
  server: {
    url: 'https://s3-ap-northeast-1.amazonaws.com/techblogrank.com/json/rankings.json',
    then: data => data.map(result => [result.rank, result.company_name, result.score, result.article_count, result.hatebu_count, result.url])
  }
}).render(document.getElementById('wrapper'))

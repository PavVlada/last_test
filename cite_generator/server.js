// function makeBib(style, item, locale) {
//     return new Promise((done, error) => {
//         loadStyle("./csl", style)
//             then(styleString => {
//                 let engine = sys.newEngine(styleString, locale, null);
//                 let items = {
//                     "0": formatItem(item)
//                 };
//                 sys.items = items;
//                 console.log(items);

//                 engine.updateItems(Object.keys(items));
//                 let bib = engine.makeBibliography();
//                 console.log("bib", bib);
//                 done(bib[1])
//             })
//             .catch(err => error(err))
//     })
// }

// const http = require('http')
// const hostname = '127.0.0.1'
// const port = 3000
// const server = http.createServer((req, res) => {
//   res.writeHead(200)
//   res.setHeader('Content-Type', 'application/json')
//   res.end(`{"message": "json response"}`)
// })
// server.listen(port, hostname, () => {
//   console.log(`Server running at http://${hostname}:${port}/`)
// })

import qs from "qs";
import fetch from "node-fetch";

let bibserverURL = "https://api.bibify.org";
let citeObject = {
  "style": "gost-r-7-0-5-2008.csl", // should be a CSL citation file (see /api/styles)
//   "type": "article", // should be a Zotero media type
  "title": "Наименование статьи",
  "authors": [{"type": "Person", "first": "Владимир", "last": "Колодезников"},
              {"type": "Person", "first": "Ефим", "last": "Колодезников"}],
  "editor": [{"type": "Person", "first": "Дамир", "last": "Дамиров"},
              {"type": "Person", "first": "Кек", "last": "Колодева"}],
  "URL": "https://google.com"
};
fetch(bibserverURL + "/api/cite?" + qs.stringify(citeObject, { format: "RFC3986"}))
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.log(err));

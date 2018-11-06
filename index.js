var ejs = require('ejs');
var fs = require('fs')
data = fs.readFileSync("globaldata.json")
pdata = JSON.parse(data)
ejs.renderFile("template.ejs", pdata, {}, function(err, str){
  fs.writeFileSync("index.html",str)      // str => Rendered HTML string
});

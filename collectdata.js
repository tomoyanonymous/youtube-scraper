var fs = require("fs");
globallist = []
folders = fs.readdirSync('./scraped_images/');
if(folders != ".DS_Store"){
for(var i =0;i<folders.length;i++){
  if(folders[i]!=".DS_Store"){
  datafilepath = './scraped_images/'+folders[i]+"/data.json"
  var content = fs.readFileSync(datafilepath);
  json = JSON.parse(content)
  globallist.push(json)
}
}
}
let data = JSON.stringify(globallist);
fs.writeFileSync('globaldata.json', data);

function doGet(e) {
  for (let p in e.parameters){
    if(p.includes('url')){
      let blob = UrlFetchApp.fetch(e.parameters[p]).getBlob();

      let folder;
      try {
        folder = DriveApp.getFoldersByName('DiscordUploads').next();
      }
      catch(e) {
        folder = DriveApp.createFolder('DiscordUploads');
      }

      folder.createFile(blob).getId();
    }
  }

  return HtmlService.createHtmlOutputFromFile("success.html")
}

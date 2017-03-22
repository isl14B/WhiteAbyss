
document.write("<table border=1><tr><th>name</th><th>description</th><th>filename</th><tr>");
for(var i=0; i<navigator.plugins.length; i++) {
    plugin = navigator.plugins[i];
    document.write("<tr><td>" + plugin.name + "</td><td>" + plugin.description + "</td><td>"  + plugin.filename + "</td><tr>");
    
}
document.write("</table>");

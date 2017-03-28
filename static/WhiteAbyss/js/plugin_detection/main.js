function main() {
    document.write("<table border=1><tr><th>name</th><th>description</th><th>filename</th><tr>");
    var plugin_info_array = [];
    for(var i=0; i<navigator.plugins.length; i++) {
        plugin = navigator.plugins[i];
    
        document.write("<tr><td>" + plugin.name + "</td><td>" + plugin.description + "</td><td>"  + plugin.filename + "</td><tr>");
        plugin_info_array.push(persePluginInfo(plugin));
    }
        execPost('./debug_page.html', JSON.stringify(plugin_info_array));
    document.write("</table>");
}    

// プラグインの情報からバージョン情報を抽出して、辞書型で返す
function persePluginInfo(pluginObj) {
    var plugin_name = pluginObj.name;
    var plugin_description = pluginObj.description;
    var plugin_version = ""

    if(plugin_name == "Shockwave Flash") {
       plugin_version =  getVersion_demo(plugin_description);
    } else {
        plugin_version = "Not found!";
    }
    return {name: plugin_name, version: plugin_version};
}

// ダミーのバージョン識別機能
function getVersion_demo(description) {
    return "0xdeadbeef";
}

// データのPOST送信機能
/*
 [reference] http://fujiiyuuki.blogspot.jp/2010/09/formjspost.html
 <a onclick="execPost('/hoge', 'data');return false;" href="#">POST送信</a>
*/
function execPost(action, data) {
 // フォームの生成
 var form = document.createElement("form");
 form.setAttribute("action", action);
 form.setAttribute("method", "post");
 form.style.display = "none";
 document.body.appendChild(form);
 // 送信データの設定
 var input = document.createElement('input');
 input.setAttribute('type', 'hidden');
 input.setAttribute('name', 'plugin_info');
 input.setAttribute('value', data);
 form.appendChild(input);
 
 // submit
 form.submit();
}

// MAIN
main();

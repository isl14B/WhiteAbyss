// プラグインに対応するバージョンチェック関数をペアで登録しておく
var VERSION_CHECK_FUNCTION_MAP = {
    "Shockwave Flash": shockwave_flash,
    "Widevine Content Decryption Module": widevine_content_decryption_module
};

function get_plugins() {
    var plugin_info_array = [];
    for(var i=0; i<navigator.plugins.length; i++) {
        var plugin = navigator.plugins[i];
        var plugin_info = extractPluginInfo(plugin);
        plugin_info_array.push(plugin_info);
    }
    var result = JSON.stringify(plugin_info_array);
    execPost("/result" , result);
}

// プラグインの情報からバージョン情報を抽出して、辞書型で返す
function extractPluginInfo(pluginObj) {
    console.log(pluginObj);
    plugin_name = pluginObj.name;
    plugin_description = pluginObj.description;
    plugin_version = "";

    // デバッグ用----------------------------------------------------------------------------------------
    // document.write(plugin_name + "<br>");
    // document.write(plugin_description+ "<br>");
    // document.write("-----------------------------<br>");
    //----------------------------------------------------------------------------------------------------

    try {
        plugin_version = VERSION_CHECK_FUNCTION_MAP[plugin_name](plugin_description);
    } catch (e) {
        plugin_version = "Not Found!"; // バージョンチェック関数が登録されていない場合
    }

    return {name: plugin_name, version: plugin_version};
}

// バージョンチェック関数群
function shockwave_flash(description) {
    return description.match(/\d+\.\d+/)[0];
}

function widevine_content_decryption_module(description) {
    return description.match(/\d+\.\d+\.\d+\.\d+/)[0]; // 1.4.8.962
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

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from lib.searchsploit_pywrap.searchsploit_pywrap import search


class TopView(generic.TemplateView):
    template_name = "top.html"


class ResultView(generic.TemplateView):
    template_name = "result.html"

    # search_word is made of name and version ==> "name version"
    @staticmethod
    def build_searchword(name, version):
        return "{} {}".format(name, version)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        # トップ画面からjson形式の脆弱性情報を受け取る
        plugins_info_list = json.loads(request.POST.get("plugin_info"))

        vulnerability_result_list = []
        vulnerability_title_dict = {}

        # 脆弱性情報をhtml形式で辞書に登録
        vulnerability_info_dict = {}

        for plugin_info_dict in plugins_info_list:
            try:
                name = plugin_info_dict.get("name")
                version = plugin_info_dict.get("version")

                # ShockWave Flash を flash に命名変更
                if name == "Shockwave Flash":
                    name = "flash"

                # デバッグ用
                # if name == "Shockwave Flash":
                #     print("*" * 20, "\nchange ShockwaveFlash -> flash\n")
                #     name = "flash"
                #     version = "10.2"
                # if name == "Widevine Content Decryption Module":
                #     name, version = 'flash', "24.0.0.186"

                # exploitDBから脆弱性情報を入手する
                search_word = self.build_searchword(name, version)
                search_result = search(search_word).get("RESULTS")

                for index, vul in enumerate(search_result):
                    # -を使わないように修正
                    vul["EDB_ID"] = vul.pop("EDB-ID")

                    title = "[" + str(vul.get("Date")) + "]<BR>" + str(vul.get("Exploit"))
                    vulnerability_title_dict.update({index: title})

                vulnerability_result_list.append([name, version, search_result])

                # 脆弱性情報の表示方法を整形
                for index, info_result in enumerate(search_result):
                    info_txt = ""
                    for k, v in info_result.items():
                        if str(k) != "Path":
                            info_txt += str(k) + ": " + str(v) + ",<BR>"
                        else:
                            info_txt += "<a href=" + "\'" + "https://www.exploit-db.com/download/" + \
                                        str(info_result.get("EDB_ID")) + "\'>" + "Poc Download" + "</a>,<BR>"
                    vulnerability_info_dict.update({index: info_txt})

            except:
                print("<!> error: searchsploit")

        context["result_list"] = vulnerability_result_list
        context["plugin_num"] = len(vulnerability_result_list)
        context["vulnerability_title_list"] = json.dumps(vulnerability_title_dict)
        context["vulnerability_info_list"] = json.dumps(vulnerability_info_dict)
        return self.render_to_response(context)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ResultView, self).dispatch(*args, **kwargs)

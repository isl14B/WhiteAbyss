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
    def buildSearchWord(self, name, version):
        return "{} {}".format(name, version)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        plugins_info_list = json.loads(request.POST.get("plugin_info"))

        result_list = []
        vulnerability_info_list = {}
        vulnerability_title_list = {}

        for plugin_info_dict in plugins_info_list:
            try:
                name = plugin_info_dict.get("name")
                version = plugin_info_dict.get("version")

                # デバッグ用
                if name == "Shockwave Flash":
                    name ,version = 'flash', "24.0.0.186"
                if name == "Java Applet Plug-in":
                    name, version = 'flash', "24.0.0.186"
                # if name == "Widevine Content Decryption Module":
                #     name, version = 'flash', "24.0.0.186"
                # if name == "QuickTime Plug-in 7.7.3":
                #     name, version = 'flash', "24.0.0.186"
                # get result of exploit_db
                search_word = self.buildSearchWord(name, version)
                search_result = search(search_word).get("RESULTS")
                for index, vul in enumerate(search_result):
                    title = "[" + str(vul.get("Date")) + "]<BR>" + str(vul.get("Exploit"))
                    vulnerability_title_list.update({index: title})
                    with open(vul.get("Path"), "r") as f:
                        vulnerability_info_list.update({index: f.read().replace("\n", "<BR>")})
                result_list.append([name, version, search_result])

            except:
                print("<!> error: searchsploit")

        context["result_list"] = result_list
        context["plugin_num"] = len(result_list)
        context["vulnerability_info_list"] = json.dumps(vulnerability_info_list)
        context["vulnerability_title_list"] = json.dumps(vulnerability_title_list)
        return self.render_to_response(context)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ResultView, self).dispatch(*args, **kwargs)

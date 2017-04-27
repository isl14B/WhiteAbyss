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
        for plugin_info_dict in plugins_info_list:
            try:
                name = plugin_info_dict.get("name")
                version = plugin_info_dict.get("version")

                # デバッグ用
                if name == "Shockwave Flash":
                    name ,version = 'flash', "24.0.0.186"
                # get result of exploit_db
                search_word = self.buildSearchWord(name, version)
                search_result = search(search_word).get("RESULTS")
                result_list.append([name, version, search_result])

            except:
                print("<!> error: searchsploit")

        context["result_list"] = result_list
        context["plugin_num"] = len(result_list)
        return self.render_to_response(context)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ResultView, self).dispatch(*args, **kwargs)

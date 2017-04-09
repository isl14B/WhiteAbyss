from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import subprocess

SEARCHSPLOIT_PATH = "/opt/exploit-database/searchsploit"


def search(plugin_name):
    cmd = "{} -j {}".format(SEARCHSPLOIT_PATH, plugin_name)

    p = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    result = p.stdout.decode('utf-8')
    return result


class TopView(generic.TemplateView):
    template_name = "top.html"


class ResultView(generic.TemplateView):
    template_name = "result.html"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        datas = json.loads(request.POST.get("plugin_info"))
        l_name = []
        l_version = []
        l_result = []

        for data in datas:
            for key, value in data.items():
                if key == "name":
                    l_name.append(value)
                elif key == "version":
                    l_version.append(value)
                else:
                    print("<!> error: data")

        for name in l_name:
            try:
                result = json.loads(search(name))
                l_result.append(result.get("RESULTS"))
            except:
                print("<!> error: searchsploit")

        context['l_plugins'] = zip(l_name, l_version, l_result)
        return self.render_to_response(context)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ResultView, self).dispatch(*args, **kwargs)

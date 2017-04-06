from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


class TopView(generic.TemplateView):
    template_name = "top.html"


class ResultView(generic.TemplateView):
    template_name = "result.html"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        datas = json.loads(request.POST.get("plugin_info"))
        l_name = []
        l_version = []

        for data in datas:
            for key, value in data.items():
                if key == "name":
                    print(value)
                    l_name.append(value)
                elif key == "version":
                    print(value)
                    l_version.append(value)
                else:
                    print("error")
            print("")

        context['l_plugins'] = zip(l_name, l_version)
        return self.render_to_response(context)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ResultView, self).dispatch(*args, **kwargs)
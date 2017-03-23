from django.views import generic


class TopView(generic.TemplateView):
    template_name = "top.html"


class ResultView(generic.TemplateView):
    template_name = "result.html"

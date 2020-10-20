from django.shortcuts import render


def create_a_crate(request):
    template = "crate/create_a_crate.html"
    context = {

    }
    return render(request, template, context)

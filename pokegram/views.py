from django.http import HttpResponse
from django.http import JsonResponse


def hello_world(request):
    return HttpResponse('El hola mundo perrito')


def test_obj(request):
    list_numbers_raw = request.GET['numbers']
    list_numbers = list_numbers_raw.split(",")
    list_int = list(map(lambda x: int(x), list_numbers))
    sorted_list = sorted(list_int)
    import pdb;
    pdb.set_trace()
    return JsonResponse(
        {
            "status": 200,
            "body": "Todo salio genial ♥"
        }
    )
    # return HttpResponse(request)


def say_hi(request, name, age):
    if age == 20:
        message = "Fua {name} sos re crack tenes 20 xD".format(name=name)
    else:
        message = "Fua {name} sos re bobina no tenes Xd".format(name=name)
    return HttpResponse(message)

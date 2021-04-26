from django.http import HttpResponse
from app.models import Product
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q


def get_page_obj(request, products):
    """
    get product from filter and put them into paginator object
    """
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    
    return paginator.get_page(page_number)


def home(request):
    """
    request.POST method will filter request and get request will show all products
    """

    if request.POST:
        dropdown_value = request.POST.get('dropdown')
        search_value = request.POST.get('search_param')

        if dropdown_value == 'Product Name':
            products = Product.objects.filter(Q(name__contains=search_value))
            page_obj = get_page_obj(request, products)
        elif dropdown_value == 'Product':
            products = Product.objects.filter(Q(type__contains=search_value))
            page_obj = get_page_obj(request, products)
        elif dropdown_value == 'Brand':
            products = Product.objects.filter(Q(brand__contains=search_value))
            page_obj = get_page_obj(request, products)
        elif dropdown_value == 'Registrant':
            products = Product.objects.filter(Q(registrant__contains=search_value))
            page_obj = get_page_obj(request, products)
        elif dropdown_value == 'Producer':
            products = Product.objects.filter(Q(producer__contains=search_value))
            page_obj = get_page_obj(request, products)

        return render(request, 'index.html', {'products': products, 'page_obj': page_obj})
    
    else:
        products = Product.objects.all()
        page_obj = get_page_obj(request, products)

        return render(request, 'index.html', {'products': products, 'page_obj': page_obj})
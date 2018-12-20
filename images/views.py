from django.shortcuts import render
from images.models import *
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage


# Create your views here.
def index(request):
    if request.method == "GET":
        imgs = []
        typelist=[]
        page_list = Page.objects.all().order_by("-id")
        type_list = Type.objects.all().order_by("id")
        for type_arr in type_list:
            type=type_arr.type
            type_id=type_arr.id
            typelist.append({"type":type,"type_id":type_id})
        for pid in page_list:
            id=pid.id
            title = pid.title
            firstimg =pid.firstimg
            sendtime = pid.sendtime
            imgs.append({"pid": id, "firstimg": firstimg, "title": title,"sendtime":sendtime})
        return render(request, 'index.html', {"data": imgs,"typelist":typelist})


def page(request, i_id):
    page_arr = Page.objects.get(id=i_id)
    imgs = []
    tags = []
    typelist = []
    time = page_arr.sendtime
    typeid = page_arr.typeid
    type = Type.objects.get(id=typeid).type
    title = page_arr.title
    pid=page_arr.id
    taglist = page_arr.tagid
    tag_arr = taglist.replace("[", "").replace("]", "").split(",")
    type_list = Type.objects.all().order_by("id")
    for type_arr in type_list:
        type = type_arr.type
        type_id = type_arr.id
        typelist.append({"type": type, "type_id": type_id})
    for t_id in tag_arr:
        tagid = t_id.strip(" ")
        tag = Tag.objects.get(id=tagid).tag
        tags.append({"tname": tag, "tid": tagid})
    imglist = Image.objects.filter(pageid=i_id)
    for img_arr in imglist:
        img = img_arr.imageurl
        imgs.append(img)
    return render(request, 'page.html',
                  {"data": imgs, "tag": tags, "title": title, "type": type, "typeid": typeid, "time": time,
                   "similar": similar(typeid),"typelist":typelist,"pid":pid,"upid":pid-1,"npid":pid+1})


def tag(request, tid):
    if request.method == "GET":
        # istagid=Tag.objects.get(tag=tag).id
        imgs = []
        typelist = []
        page_list = Page.objects.all().order_by("-id")
        type_list = Type.objects.all().order_by("id")
        for type_arr in type_list:
            type = type_arr.type
            type_id = type_arr.id
            typelist.append({"type": type, "type_id": type_id})
        for pid in page_list:
            if tid in pid.tagid:
                id=pid.id
                title = pid.title
                firstimg = pid.firstimg
                sendtime = pid.sendtime
                imgs.append({"pid": id, "firstimg": firstimg, "title": title, "sendtime": sendtime})
        return render(request, 'index.html', {"data": imgs,"typelist":typelist})


def type(request, typeid):
    if request.method == "GET":
        imgs = []
        typelist = []
        type_list = Type.objects.all().order_by("id")
        for type_arr in type_list:
            type = type_arr.type
            type_id = type_arr.id
            typelist.append({"type": type, "type_id": type_id})
        page_list = Page.objects.filter(typeid=typeid).order_by("-id")
        for pid in page_list:
            title = pid.title
            firstimg = pid.firstimg
            id=pid.id
            sendtime = pid.sendtime
            imgs.append({"pid": id, "firstimg": firstimg, "title": title, "sendtime": sendtime})
        return render(request, 'index.html', {"data": imgs,"typelist":typelist})


def similar(id):
    similarlist = []
    sidlist = Page.objects.filter(typeid=id).order_by("-id")
    i = 0
    for s in sidlist:
        if i < 6:
            stitle = s.title
            pid = s.id
            tid = s.typeid
            similarlist.append({"stitle": stitle, "tid": tid, "pid": pid})
            i += 1
    return similarlist


def search(request):
    if request.method == "POST":
        imgs = []
        typelist = []
        type_list = Type.objects.all().order_by("id")
        for type_arr in type_list:
            type = type_arr.type
            type_id = type_arr.id
            typelist.append({"type": type, "type_id": type_id})
        context = request.POST['s']
        pagelist = Page.objects.filter(title__contains=context).order_by("-id")
        for page in pagelist:
            title = page.title
            id=page.id
            firstimg = page.firstimg
            sendtime = page.sendtime
            imgs.append({"pid": id, "firstimg": firstimg, "title": title, "sendtime": sendtime})
        return render(request, 'index.html', {"data": imgs,"typelist":typelist})

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Profile, T_View, Following
from django.contrib.auth.models import User
from django.conf import settings
import json
from django.views import View
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from django.core.paginator import Paginator


@login_required(login_url='login')
def patientHomeView(request):
    # # order_by('-pk') is for ordering the posts in decending order of their id
    user = Following.objects.get(user = request.user)
    
    followed_users = user.followed.all()

    posts = Post.objects.filter(user__in=followed_users).order_by('-pk') | Post.objects.filter(user=request.user).order_by('-pk')
    viewed_ = [
        i for i in posts if T_View.objects.filter(post=i, user=request.user)
    ]
    data = {
        'posts': posts,
        "viewed_post": viewed_
    }
    return render(request, "patient/patient_newsfeed.html", data)
    

@login_required(login_url='login')
def postViews(request):
    if request.method == "POST":
        image_ = request.FILES['image']
        captions_ = request.POST.get('captions')
        user_ = request.user
        post_obj = Post(user=user_, caption=captions_, image=image_)
        post_obj.save()
        messages.success(request, "Post created successfully!!!")
        return redirect('/patient')
    else:
        messages.error(request, "Something went wrong:(")
        return redirect('/patient')


@login_required(login_url='login')
def deletePostView(request, ID):  # specific id for specific post
    del_post = Post.objects.filter(pk=ID)
    image_path = del_post[0].image.url  # image location in system
    del_post.delete()
    messages.info(request, 'Post has been deleted:(')
    return redirect('/patient')


@login_required(login_url='login')
def userProfileView(request, username):
    user = User.objects.filter(username=username)
    if user:
        user = user[0]
        profile = Profile.objects.get(user=user)
        post = getPost(user)
        bio = profile.bio
        user_img = profile.userImage
        is_following = Following.objects.filter(user = request.user, followed = user)
        #create a following object
        following_obj = Following.objects.get(user = user)
        follower, following = following_obj.follower.count(), following_obj.followed.count()
        data = {
            'user_obj': user,
            'bio': bio,
            'follower': follower,
            'following': following,
            'userImg': user_img,
            'posts': post,
            'connection':is_following
        }
    else:
        return HttpResponse("No Such User")
    return render(request, 'patient/patientProfile.html', data)


def getPost(user):
    post_obj = Post.objects.filter(user=user)
    imgList = [
        post_obj[i:i+3] for i in range(0, len(post_obj), 3)
    ]
    return imgList
@login_required(login_url='login')
def viewPost(request):
    id = request.GET.get("viewId", "")
    post = Post.objects.get(pk=id)
    user = request.user
    view = T_View.objects.filter(post=post, user=user)
    viewed = False

    if view:
        T_View.ignore(post, user)
    else:
        viewed=True
        T_View.viewed(post, user)
    resp = {
        'viewed':viewed
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type = "application/json")


@login_required(login_url='login')
def follow(request, username):
    main_user = request.user
    to_follow = User.objects.get(username = username)

    #check if already following
    following = Following.objects.filter(user = main_user, followed = to_follow)
    is_following = True if following else False



    if is_following:
        #then unfollow the user
        Following.unfollow(main_user, to_follow)
        is_following = False
    else:
        Following.follow(main_user, to_follow)
        is_following = True
    
    resp = {
        "following" : is_following,
    }

    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")

class SearchUserView(ListView):
    model = User
    template_name = "patient/searchUser.html"

    paginate_by = 5

    def get_queryset(self):
        username = self.request.GET.get("username", "")
        queryset = User.objects.filter(username__icontains = username)
        return queryset


class EditProfile(View):
    def post(self, request, *args, **kwargs):
        profile_obj = Profile.objects.get(user=request.user)
        bio = request.POST.get("Bio", "")
        img = request.FILES.get("image", "")
        if bio:
            profile_obj.bio = bio
        if img:
            profile_obj.userImage = img
        profile_obj.save()

        return HttpResponseRedirect(reverse("patient:userProfileView", args=(request.user.username,)))


class LabReportView(TemplateView):
    template_name = "patient/lab_report.html"


class PrescriptionView(TemplateView):
    template_name = "patient/prescription.html"


class DrugListView(TemplateView):
    template_name = "patient/drug_list.html"


class AllDiseaseView(TemplateView):
    template_name = "patient/disease.html"


class AppointmentView(TemplateView):
    template_name = "patient/appointment.html"


class CheckoutView(TemplateView):
    template_name = "patient/checkout.html"


class Documentation(TemplateView):
    template_name = "patient/documentation.html"

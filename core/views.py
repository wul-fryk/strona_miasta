from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages


from posts.models import Post, Like, Dislike, Account, Coment, Interractions
# Create your views here.

def home(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'core/home.html', context)

def search(request):    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    if q == '':
        messages.info(request, 'Wprowadzono puste zapytanie.')
        return redirect('home')
    people = Account.objects.filter(
        Q(username__icontains=q)
    )
    posts = Post.objects.filter(
        Q(title__icontains=q) |
        Q(body__icontains=q)   
    )
    context = {'posts':posts, 'people':people, 'posts':posts}
    return render(request, 'core/search_results.html', context)

def post(request, pk):
    post_infos = Post.objects.get(id=pk)
    try:
        user_likes = Like.objects.get(post=post_infos, person=request.user)
    except:
        user_likes = None
    try:
        user_dislikes = Dislike.objects.get(post=post_infos, person=request.user)
    except:
        user_dislikes = None

    coments = Coment.objects.filter(comented_post=pk)
    context = {'post_infos':post_infos, 'user_likes':user_likes, 'user_dislikes':user_dislikes, 'coments':coments}
    return render(request, 'core/post.html', context)

def like_func(request, pk):
    post_req = Post.objects.get(id=pk)
    if request.method == "POST":
        #check if user aleready dilikes the post, then unduslike
        if Dislike.objects.filter(post=pk, person=request.user.id).exists() is True:
            dislike = Dislike.objects.get(post=pk, person=request.user.id)
            dislike.delete()
            post_req.save()
            post_req.reactions += 1
            check_interactions(request.user, post_req, 'dd')
        #check if user already likes the post, then unlike
        if Like.objects.filter(post=pk, person=request.user.id).exists() is True:
            like = Like.objects.get(post=pk, person=request.user.id)
            like.delete()
            post_req.reactions -= 1
            post_req.save()
            check_interactions(request.user, post_req, 'ld')
            return redirect('post', pk)
        #add like to post
        else:
            Like.objects.create(
                person = Account.objects.get(id=request.user.id),
                post = post_req
            )
            post_req.reactions += 1
            post_req.save()
            check_interactions(request.user, post_req, 'la')
            return redirect('post', pk)

def dislike_func(request, pk):
    post_req = Post.objects.get(id=pk)
    if request.method == "POST":
        #check if user aleready likes the post, then unlike
        if Like.objects.filter(post=pk, person=request.user.id).exists() is True:
            like = Like.objects.get(post=pk, person=request.user.id)
            like.delete()
            post_req.reactions -= 1
            post_req.save()
            check_interactions(request.user, post_req, 'ld')
        #check if user already dislikes the post, then undislike
        if Dislike.objects.filter(post=pk, person=request.user.id).exists() is True:
            dislike = Dislike.objects.get(post=pk, person=request.user.id)
            dislike.delete()
            post_req.reactions += 1
            post_req.save()
            check_interactions(request.user, post_req, 'dd')
            return redirect('post', pk)
        #add dislike to post
        else:
            Dislike.objects.create(
                person = Account.objects.get(id=request.user.id),
                post = post_req
            )
            post_req.reactions -= 1
            post_req.save()
            check_interactions(request.user, post_req, 'da')
            return redirect('post', pk)


def user_page(request, name):
    user_req = Account.objects.get(username = name)
    posts = Post.objects.filter(owner = user_req.id)
    context = {'user_req':user_req, 'posts':posts}

    return render(request, 'core/user_page.html', context)

def check_interactions(user, post_id, status):
    if status in ['ca', 'la', 'da']:                                                                 #If user wants to add interaction, but there alredy exist then adds nothing
        try:
            Interractions.objects.get(person=user, post=post_id)
        except:
            Interractions.objects.create(
                person = user,
                post = post_id
            )
        return True                                                                              

    like_status = False                                                                            #If there is no coment thent like status is False
    try:
        Like.objects.get(post=post_id, person=user)
    except:
        like_status = True
    dislike_status = False
    try:
        Dislike.objects.get(post=post_id, person=user)
    except:
        dislike_status = True
    coment_status = False
    try:
        Coment.objects.get(owner=user, comented_post=post_id)
    except:
        coment_status = True
    print(like_status, dislike_status, coment_status, status)

    if status == 'ld':
        if (dislike_status is True) and (coment_status is True):                                   #If user want to delete like, but there already exists dislike or coment then return nothing
            iter = Interractions.objects.get(person=user, post=post_id)
            iter.delete()
        return True
    if status == 'dd':
        if (like_status is True) and (coment_status is True):
            iter = Interractions.objects.get(person=user, post=post_id)
            iter.delete()
        return True
    if status == 'cd':
        if (like_status is True) and (dislike_status is True):
            iter = Interractions.objects.get(person=user, post=post_id)
            iter.delete()
        return True

def user_interactions(request, username):
    user_req = Account.objects.get(username=username)
    context = {'user_req':user_req}
    return render(request, 'core/user_post_interactions.html', context)
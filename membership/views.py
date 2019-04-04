from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from .forms import LoginForm,RegisterForm
from django.contrib.auth import (authenticate, 
                                 login,
                                logout,
                                 update_session_auth_hash)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth.forms import PasswordChangeForm

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('basic:home'))
    form = LoginForm(request.POST or None)
    context = {'form': form,'onLogin':True}

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.INFO, 'Successfully Logged in !')
                return HttpResponseRedirect(reverse('basic:home'))


    return render(request, 'membership/login.html', context)



def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.add_message(request, messages.INFO, "Successfully Logged Out")
        return HttpResponseRedirect(reverse('basic:home'))
    else:
        messages.add_message(request, messages.INFO, "You were not logged in.")
        return HttpResponseRedirect(reverse('basic:home'))

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            try:
                course = request.POST['course']
                if course == None or course == '':
                    new_user = form.save()
                    new_user = authenticate(username=form.cleaned_data['username'],
                                                                            password=form.cleaned_data['password1'],
                                                                            )
                    login(request, new_user)
                    return HttpResponseRedirect(reverse('basic:home'))
 
                elif str(course.lower()) == 'jito':
                    new_user = form.save(course = course)

                    new_user = authenticate(username=form.cleaned_data['username'],
                                                                            password=form.cleaned_data['password1'],
                                                                            )
                    login(request, new_user)
                    return HttpResponseRedirect(reverse('basic:jitoHome'))
                elif str(course).lower() == 'siel':
                    new_user = form.save(course = course)

                    new_user = authenticate(username=form.cleaned_data['username'],
                                                                            password=form.cleaned_data['password1'],
                                                                            )
                    login(request, new_user)
                    return HttpResponseRedirect(reverse('basic:studentInfo'))
                elif str(course).lower() == 'jen':
                    new_user = form.save(course = course)
                    new_user = authenticate(username=form.cleaned_data['username'],
                                                                            password=form.cleaned_data['password1'],
                                                                            )

                    login(request,new_user)
                    return HttpResponseRedirect(reverse('basic:studentInfo'))
                elif str(course).lower() == 'ysm':
                    new_user = form.save(course = course)
                    new_user = authenticate(username=form.cleaned_data['username'],
                                                                            password=form.cleaned_data['password1'],
                                                                            )

                    login(request,new_user)
                    return HttpResponseRedirect(reverse('basic:studentInfo'))


                else:
                    new_user = form.save()
                    new_user = authenticate(username=form.cleaned_data['username'],
                                                                            password=form.cleaned_data['password1'],
                                                                            )
                    login(request, new_user)
                    return HttpResponseRedirect(reverse('basic:home'))
 

            

            except Exception as e:
               print(str(e)) 
            new_user = form.save()
            
            new_user = authenticate(username=form.cleaned_data['username'],
                                                                        password=form.cleaned_data['password1'],
                                                                        )
            login(request, new_user)
            return HttpResponseRedirect(reverse('basic:home'))
        else:
            context = {'form':form}
            return render(request,'membership/register.html', context)
    else:
        form = RegisterForm()
        context = {'form':form}
        return render(request,'membership/register.html',context)



def user_changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST,user = request.user)

        if form.is_valid():
            form.save()
            messages.success(request,'Password successfully changed !!')
            update_session_auth_hash(request,form.user)
            return HttpResponseRedirect(reverse('basic:home'))
    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form':form}
    return render(request,'membership/change_password.html',context)

#--------------------------------------------------------------------------------------------------
# client user logins

def siel_user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('basic:home'))
    form = LoginForm(request.POST or None)
    context = {'form': form,'onLogin':True}

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.INFO, 'Successfully Logged in !')
                return HttpResponseRedirect(reverse('basic:home'))


    return render(request, 'membership/siel_login.html', context)


#--------------------------------------------------------------------------------------------------

def srw_user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('basic:home'))
    form = LoginForm(request.POST or None)
    context = {'form': form,'onLogin':True}

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.INFO, 'Successfully Logged in !')
                return HttpResponseRedirect(reverse('basic:home'))


    return render(request, 'membership/swami_login.html', context)

#---------------------------------------------------------------------------------------------
def jen_user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('basic:home'))
    form = LoginForm(request.POST or None)
    context = {'form': form,'onLogin':True}

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.INFO, 'Successfully Logged in !')
                return HttpResponseRedirect(reverse('basic:home'))


    return render(request, 'membership/jen_login.html', context)

#---------------------------------------------------------------------------------------------
def ysm_user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('basic:home'))
    form = LoginForm(request.POST or None)
    context = {'form': form,'onLogin':True}

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.INFO, 'Successfully Logged in !')
                return HttpResponseRedirect(reverse('basic:home'))


    return render(request, 'membership/ysm_login.html', context)



#---------------------------------------------------------------------------------------------

# client user logouts

def siel_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.add_message(request, messages.INFO, "Successfully Logged Out")
        return HttpResponseRedirect(reverse('membership:SielLogin'))
    else:
        messages.add_message(request, messages.INFO, "You were not logged in.")
        return HttpResponseRedirect(reverse('membership:SielLogin'))

def srw_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.add_message(request, messages.INFO, "Successfully Logged Out")
        return HttpResponseRedirect(reverse('membership:SwamiLogin'))
    else:
        messages.add_message(request, messages.INFO, "You were not logged in.")
        return HttpResponseRedirect(reverse('membership:SwamiLogin'))

def jen_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.add_message(request, messages.INFO, "Successfully Logged Out")
        return HttpResponseRedirect(reverse('membership:JENLogin'))
    else:
        messages.add_message(request, messages.INFO, "You were not logged in.")
        return HttpResponseRedirect(reverse('membership:JENLogin'))

def ysm_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.add_message(request, messages.INFO, "Successfully Logged Out")
        return HttpResponseRedirect(reverse('membership:YSMLogin'))
    else:
        messages.add_message(request, messages.INFO, "You were not logged in.")
        return HttpResponseRedirect(reverse('membership:YSMLogin'))








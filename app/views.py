from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    profile = Profile.objects.filter(user = request.user).first()
    expenses = Expense.objects.filter(user = request.user)
    if request.method == 'POST':
        text = request.POST.get('text')
        amount = request.POST.get('amount')
        expense_type = request.POST.get('expense_type') 

        expense = Expense(name=text , amount=amount , expense_type=expense_type , user= request.user)
        expense.save()
        
        if expense_type == 'Positive':
            profile.balance += float(amount)
            profile.income+= float(amount)
        else:
            profile.expenses += float(amount)
            profile.balance -= float(amount)
            
        profile.save()
        return redirect('/home')
    
    elif request.method == 'GET' and 'delete_id' in request.GET:
        delete_id = request.GET['delete_id']
        expense_to_delete = get_object_or_404(Expense, id=delete_id, user=request.user)
        amount_to_delete = expense_to_delete.amount

        if expense_to_delete.expense_type == 'Positive':
            profile.balance -= float(amount_to_delete)
            profile.income -= float(amount_to_delete)
        else:
            profile.expenses -= float(amount_to_delete)
            profile.balance += float(amount_to_delete)

        profile.save()
        expense_to_delete.delete()
        return redirect('/home')


    context = {'profile' : profile , 'expenses' : expenses , 'username': request.user.username}
    return render(request , 'home.html' , context)

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if len(uname) < 5:
            error_message = "Username must be at least 5 characters long!!"
            return render(request, 'signup.html', {'error_message': error_message})
        
        if len(pass1) < 8:
            error_message = "Password must be at least 8 characters long!!"
            return render(request, 'signup.html', {'error_message': error_message})


        if pass1 != pass2:
            error_message = "Your password and confirm password do not match!!"
            return render(request, 'signup.html', {'error_message': error_message})

        try:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            messages.success(request, 'Your account has been created successfully!')
            return render(request, 'signup.html', {'redirect_delay': True})
        
        except:
            error_message = "An error occurred during account creation. Please try again."
            return render(request, 'signup.html', {'error_message': error_message})

    return render(request, 'signup.html')
        

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            # Check if the user is logging in for the first time
            is_first_login = not Profile.objects.filter(user=user).exists()
            
            # Create or update the user's profile
            profile, created = Profile.objects.get_or_create(user=user)
            
            if is_first_login:
                # Perform initial profile update for first-time login
                profile.income = 0
                profile.expenses = 0
                profile.balance = 0
                profile.save()
            
            # Retrieve the previous data for returning users
           
            
            return redirect('home')
        else:
             error_message = "Username or password is invalid !!"
             return render(request, 'login.html', {'error_message': error_message})

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')
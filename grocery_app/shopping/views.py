import paypalrestsdk
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import GroceryItem, Payment
from django import forms
from django.conf import settings

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})

api = paypalrestsdk.Api({
    'mode': 'sandbox',  # or 'live'
    'client_id': 'AaQ6G027gCWn-KGipYjvh41UBnVey0d_IK7U6u9XikGqmtavSJ6lDXu20n--03-tzYLC60VjjaMqcMrG',
    'client_secret': 'EAY8ThfNMyJgVXhVSWXON32FrZLJgL_CeT43uOupxmUYbgfvNgGq8FarhWQt8hQwKl0HsMBwDpOYj4m2'
})

try:
    token = api.get_token()
    print("Token retrieved successfully:", token)
except Exception as e:
    print("Error retrieving token:", str(e))

# Updated Form
class GroceryItemForm(forms.ModelForm):
    class Meta:
        model = GroceryItem
        fields = ['name', 'quantity', 'price']

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('grocery_list')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def grocery_list(request):
    items = GroceryItem.objects.filter(user=request.user)
    form = GroceryItemForm()
    total_cost = sum(item.total_cost for item in items.filter(purchased=True))

    if request.method == 'POST':
        if 'add' in request.POST:
            form = GroceryItemForm(request.POST)
            if form.is_valid():
                item = form.save(commit=False)
                item.user = request.user
                item.save()
                return redirect('grocery_list')
        elif 'delete' in request.POST:
            item_id = request.POST.get('item_id')
            GroceryItem.objects.filter(id=item_id, user=request.user).delete()
            return redirect('grocery_list')
        elif 'toggle' in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(GroceryItem, id=item_id, user=request.user)
            item.purchased = not item.purchased
            item.save()
            return redirect('grocery_list')

    return render(request, 'grocery_list.html', {'items': items, 'form': form, 'total_cost': total_cost})

@login_required
def edit_item(request, item_id):
    item = get_object_or_404(GroceryItem, id=item_id, user=request.user)
    if request.method == 'POST':
        form = GroceryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('grocery_list')
    else:
        form = GroceryItemForm(instance=item)
    return render(request, 'edit_item.html', {'form': form, 'item': item})

@login_required
def payment_page(request):
    items = GroceryItem.objects.filter(user=request.user, purchased=True)
    total_cost = sum(item.total_cost for item in items)
    
    if request.method == 'POST' and 'create_payment' in request.POST:
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": request.build_absolute_uri('/payment_execute/'),
                "cancel_url": request.build_absolute_uri('/grocery_list/'),
            },
            "transactions": [{
                "amount": {
                    "total": f"{total_cost:.2f}",
                    "currency": "USD",
                },
                "description": "Payment for grocery items",
            }],
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    return redirect(link.href)
        else:
            messages.error(request, "Error creating payment. Please try again.")
            return redirect('payment_page')

    return render(request, 'payment_page.html', {'items': items, 'total_cost': total_cost})

@login_required
def payment_execute(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    if not payment_id or not payer_id:
        messages.error(request, "Payment was cancelled or invalid.")
        return redirect('grocery_list')

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        # Save payment record
        Payment.objects.create(
            user=request.user,
            paypal_payment_id=payment_id,
            amount=payment.transactions[0].amount.total,
            status='completed'
        )
        # Clear purchased items
        GroceryItem.objects.filter(user=request.user, purchased=True).delete()
        messages.success(request, f"Payment of ${payment.transactions[0].amount.total} completed successfully!")
        return redirect('grocery_list')
    else:
        messages.error(request, "Payment execution failed.")
        return redirect('grocery_list')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'logout_confirm.html')
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import (
    CustomPasswordChangeForm,
    PendingInvoiceForm,
    SecretAnswerForm,
    UsernameForm,
    UserRegisterForm,
)
from .models import ApprovedInvoice, PendingInvoice

User = get_user_model()


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("invoice_list")
    else:
        form = UserRegisterForm()
    return render(request, "billing/register.html", {"form": form})


def password_reset(request):
    if request.method == "POST":
        form = UsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            try:
                user = User.objects.get(username=username)
                request.session["reset_user_id"] = user.id
                return redirect("password_reset_secret")
            except User.DoesNotExist:
                form.add_error("username", "User does not exist.")
    else:
        form = UsernameForm()
    return render(request, "billing/password_reset.html", {"form": form})


def password_reset_secret(request):
    user_id = request.session.get("reset_user_id")
    if not user_id:
        return redirect("password_reset")

    user = User.objects.get(id=user_id)
    if request.method == "POST":
        form = SecretAnswerForm(request.POST)
        if form.is_valid():
            secret_answer = form.cleaned_data["secret_answer"]
            new_password = form.cleaned_data["new_password"]
            if user.secret_answer == secret_answer:
                user.password = make_password(new_password)
                user.save()
                return redirect("login")
            else:
                form.add_error("secret_answer", "Incorrect secret answer.")
    else:
        form = SecretAnswerForm()

    return render(
        request, "billing/password_reset_secret.html", {"form": form, "secret_question": user.secret_question}
    )


@login_required
def invoice_list(request):
    return render(request, "billing/invoice_list.html")


@login_required
def create_invoice(request):
    if request.method == "POST":
        form = PendingInvoiceForm(request.POST)
        if form.is_valid():
            pending_invoice = form.save(commit=False)
            pending_invoice.sender = request.user
            pending_invoice.save()
            return redirect("invoice_list")
    else:
        form = PendingInvoiceForm()
    return render(request, "billing/create_invoice.html", {"form": form})


@login_required
def approve_invoice(request, pk):
    invoice = PendingInvoice.objects.get(pk=pk)
    if request.method == "POST":
        ApprovedInvoice.objects.create(
            sender=invoice.sender, receiver=invoice.receiver, amount=invoice.amount, description=invoice.description
        )
        invoice.delete()
        return redirect("invoice_list")
    return render(request, "billing/approve_invoice.html", {"invoice": invoice})


@login_required
def sent_pending_invoices(request):
    invoices = PendingInvoice.objects.filter(sender=request.user)
    return render(request, "billing/sent_pending_invoices.html", {"invoices": invoices})


@login_required
def sent_approved_invoices(request):
    invoices = ApprovedInvoice.objects.filter(sender=request.user)
    return render(request, "billing/sent_approved_invoices.html", {"invoices": invoices})


@login_required
def approve_invoice(request, pk):
    invoice = get_object_or_404(PendingInvoice, pk=pk)
    if request.method == "POST":
        ApprovedInvoice.objects.create(
            sender=invoice.sender,
            receiver=invoice.receiver,
            amount=invoice.amount,
            description=invoice.description,
            date_created=invoice.date_created,
        )
        invoice.delete()
        return redirect("sent_pending_invoices")  # 承認後に sent_pending_invoices へリダイレクト
    return render(request, "billing/approve_invoice.html", {"invoice": invoice})


@login_required
def received_pending_invoices(request):
    invoices = PendingInvoice.objects.filter(receiver=request.user)
    return render(request, "billing/received_pending_invoices.html", {"invoices": invoices})


@login_required
def received_approved_invoices(request):
    invoices = ApprovedInvoice.objects.filter(receiver=request.user)
    return render(request, "billing/received_approved_invoices.html", {"invoices": invoices})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def password_change(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("password_change_done")
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, "registration/password_change_form.html", {"form": form})


@login_required
def password_change_done(request):
    return render(request, "registration/password_change_done.html")

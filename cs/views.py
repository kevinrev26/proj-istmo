from django.shortcuts import render, redirect
from .forms import CustomerSupportTicketForm
from django.contrib import messages


def create_ticket(request):
    template_data = {}
    template_data['title'] = 'Create customer support ticket'
    if request.method == 'GET':
        form = CustomerSupportTicketForm()
        template_data['form'] = form
        return render(request, 'cs/create_cs_ticket.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomerSupportTicketForm(request.POST, request.FILES)
        if form.is_valid():
            cs_ticket = form.save(commit=False)
            cs_ticket.user = request.user
            cs_ticket.save()
            messages.success(request, f'Ticket {cs_ticket.ticket_number} was successfully created.')
            return redirect('home.index')
        else:
            template_data['form'] = form
            return render(request, 'cs/create_cs_ticket.html', {'template_data': template_data})
from collections import OrderedDict
from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail as django_send_mail
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from functools import reduce
from import_export import widgets
from hashlib import md5
from operator import or_ as OR
from smtplib import SMTPSenderRefused

# import datetime
# import re


class BooleanWidget(widgets.Widget):
    """
    Convert strings to boolean values
    """

    def clean(self, value):
        if value == 'Yes':
            return True
        else:
            return False


class DecimalWidget(widgets.Widget):
    """
    Convert strings to decimal values
    """

    def clean(self, value):
        if value:
            return Decimal(value.replace(',', ''))
        else:
            return Decimal(0)


class UserWidget(widgets.Widget):
    """
    """

    def clean(self, value):
        return value


def add_user_to_contacts(request, model, pk=None):
    """
    """
    if request.method == 'POST':
        if pk is None:
            return HttpResponseRedirect(reverse('user_index'))
        else:
            contact = request.POST.get('contact')
            user = get_object_or_404(User, pk=pk)
            if not user.email or not user.first_name or not user.last_name:
                messages.add_message(request, messages.WARN,
                                     'No email no contact!')
                return HttpResponseRedirect(reverse('user_index'))
            contact = model(
                email=user.email,
                active=True,
                first_name=user.first_name,
                last_name=user.last_name)
            contact.save()
            messages.add_message(request, messages.INFO,
                                 'User added to contacts!')
            return HttpResponseRedirect(reverse('contact_index'))


def class_name_pk(self):
    """
    Concatenate class name and id
    """
    return '-'.join([self.__class__.__name__.lower(), str(self.pk)])


def daily_burn(project):
    try:
        days = (project.end_date - project.start_date).days
        hours = project.budget
        burn = hours / days
        return '%.2f' % burn
    except (TypeError, ZeroDivisionError):
        return ''


def dashboard_items(model, active=True, hidden=False, order_by=None):
    """
    """
    items = model.objects.filter(active=active, hidden=hidden)
    if order_by:
        items = items.order_by(order_by)
    return items


def dashboard_totals(model):
    results = OrderedDict()
    invoices_active = model.objects.filter(last_payment_date=None)
    invoices_active = invoices_active.order_by('-pk')
    gross = 0
    net = 0
    for invoice in invoices_active:
        results[invoice] = {}
        results[invoice]['subtotal'] = invoice.subtotal
        results[invoice]['amount'] = invoice.amount
        if invoice.subtotal:
            gross += invoice.subtotal
        if invoice.amount:
            net += invoice.amount
    return gross, net


def edit(request,
         form_model,
         model,
         url_name,
         template,
         amount=None,
         client=None,
         clients=[],
         company=None,
         context={},
         gross=None,
         kwargs={},
         active_nav=None,
         net=None,
         pk=None,
         paid_amount=None,
         paid=None,
         project=None,
         projects=[],
         subtotal=None,
         task=None,
         tasks=[]):
    obj = None
    if pk is None:
        form = form_model()
        # Populate new report with gross and net calculated
        # from active invoices
        if form._meta.model._meta.verbose_name == 'report':
            obj = model(gross=gross, net=net)
            form = form_model(instance=obj)
        # Limit time entry project, client
        # and task choices
        if form._meta.model._meta.verbose_name == 'time':
            form.fields['project'].queryset = projects
            form.fields['client'].queryset = clients
            form.fields['task'].queryset = tasks
        # Limit project client choices
        if form._meta.model._meta.verbose_name == 'project':
            form.fields['client'].queryset = clients
        # Populate time entry form fields with project, client
        # and task values
        if project and model._meta.verbose_name == 'time':
            entry = model(
                project=project, client=project.client, task=project.task)
            form = form_model(instance=entry)
        # Populate invoice with project
        elif project and model._meta.verbose_name == 'invoice':
            entry = model(project=project, client=project.client)
            form = form_model(instance=entry)
        # Populate time entry form fields with client and
        # task values
        elif client and task:
            entry = model(client=client, task=task)
            form = form_model(instance=entry)
        # Populate project entry form fields with client value
        elif client:
            entry = model(client=client)
            form = form_model(instance=entry)
        # Populate time entry form fields with task value
        elif task:
            entry = model(task=task)
            form = form_model(instance=entry)
    else:
        obj = get_object_or_404(model, pk=pk)
        form = form_model(instance=obj)
    if request.method == 'POST':
        ref = request.META['HTTP_REFERER']
        if pk is None:
            form = form_model(request.POST)
        else:
            copy = request.POST.get('copy')
            delete = request.POST.get('delete')
            if copy:
                dup = obj
                dup.pk = None
                dup.save()
                kwargs = {}
                kwargs['pk'] = dup.pk
                if obj._meta.verbose_name == 'time':
                    url_name = 'entry_edit'
                return HttpResponseRedirect(reverse(url_name, kwargs=kwargs))
            if delete:
                url_name = None
                # Decrement invoice counter
                if (obj._meta.verbose_name == 'invoice' and
                        company.invoice_counter):
                    company.invoice_counter -= 1
                    company.save()
                # Decrement estimate counter
                if (obj._meta.verbose_name == 'estimate' and
                        company.estimate_counter):
                    company.estimate_counter -= 1
                    company.save()
                # Redir to appropriate location
                url_name = url_name_from(obj._meta.verbose_name)
                if (obj._meta.verbose_name == 'time' and
                        not request.user.is_staff):
                    url_name = 'home'
                obj.delete()
                return HttpResponseRedirect(reverse(url_name))
            checkbox = request.POST.get('checkbox')
            checkbox_publish = request.POST.get('checkbox-publish')
            if checkbox == 'on' or checkbox == 'off':
                kwargs = {}
                if checkbox == 'on':
                    obj.active = True
                else:
                    obj.active = False
                obj.save()
                return HttpResponseRedirect(ref)
            if checkbox_publish == 'on' or checkbox_publish == 'off':
                kwargs = {}
                if checkbox_publish == 'on':
                    obj.published = True
                else:
                    obj.published = False
                obj.save()
                # Redir to appropriate index for checkbox_publish
                url_name = url_name_from(obj._meta.verbose_name)
                return HttpResponseRedirect(reverse(url_name, kwargs=kwargs))
            if amount and subtotal and paid_amount and paid:
                obj.amount = amount
                obj.last_payment_date = timezone.now()
                obj.subtotal = subtotal
                obj.paid_amount = paid_amount
                obj.save()
                return HttpResponseRedirect(reverse(url_name, kwargs=kwargs))
            elif amount and subtotal and paid_amount:
                obj.amount = amount
                obj.subtotal = subtotal
                obj.paid_amount = paid_amount
                obj.save()
                return HttpResponseRedirect(reverse(url_name, kwargs=kwargs))
            elif amount and subtotal:
                obj.amount = amount
                obj.subtotal = subtotal
                obj.save()
                return HttpResponseRedirect(reverse(url_name))
            elif amount:
                obj.amount = amount
                obj.save()
                return HttpResponseRedirect(reverse(url_name))
            form = form_model(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save()
            # Time entry
            if obj.__class__.__name__ == 'Time' and pk is None:
                # Assign user to time entry on creation
                obj.user = User.objects.get(username=request.user)
                obj.save()
                # Send mail when time entry created
                if hasattr(obj.user, 'profile'):
                    if obj.user.profile.notify:
                        subject = 'Time entry'
                        message = '%s entered time! %s' % (
                            obj.user.username,
                            obj.get_absolute_url(request.get_host()))
                        send_mail(request, subject, message,
                                  settings.DEFAULT_FROM_EMAIL)
            # Assign and increment invoice counter
            if (obj._meta.verbose_name == 'invoice' and
                    company.invoice_counter and pk is None):
                company.invoice_counter += 1
                company.save()
                obj.document_id = company.invoice_counter
                obj.save()
            # Assign and increment estimate counter
            if (obj._meta.verbose_name == 'estimate' and
                    company.estimate_counter and pk is None):
                company.estimate_counter += 1
                company.save()
                obj.document_id = company.estimate_counter
                obj.save()
            # Assign client to invoice
            if obj._meta.verbose_name == 'invoice' and obj.project:
                if obj.project.client and not obj.client:
                    obj.client = obj.project.client
                    obj.save()
            return HttpResponseRedirect(reverse(url_name, kwargs=kwargs))
    context['item'] = obj
    context['form'] = form
    context['active_nav'] = active_nav
    context['pk'] = pk
    return render(request, template, context)


def entries_total(queryset):
    """
    Add estimate and invoice time entries, could be an aggregate
    (https://docs.djangoproject.com/en/1.9/topics/db/aggregation/)
    """
    entries = OrderedDict()
    total = 0
    running_total_co = 0
    running_total_dev = 0
    running_total_hours = 0
    for entry in queryset:
        entries[entry] = {}
        hours = entry.hours
        if hours:
            running_total_hours += hours
        entries[entry]['date'] = entry.date
        entries[entry]['hours'] = hours
        entries[entry]['notes'] = entry.notes
        entries[entry]['pk'] = entry.pk
        entries[entry]['user'] = entry.user
        entries[entry]['task'] = entry.task
        line_total = 0
        line_total_co = 0
        line_total_dev = 0
        line_total_client = 0
        if entry.task:
            rate = entry.task.rate
            entries[entry]['rate'] = rate
            if rate:
                line_total_co = rate * hours
            entries[entry]['line_total_co'] = line_total_co
            running_total_co += line_total_co
        if entry.user and entry.project:
            if hasattr(entry.user, 'profile'):
                if entry.user.profile.rate:
                    line_total_dev = entry.user.profile.rate * hours
                entries[entry]['line_total_dev'] = line_total_dev
                running_total_dev += line_total_dev
        if entry.project:
            line_total = line_total_co - line_total_dev
            line_total_client = line_total_co
            entries[entry]['line_total_client'] = '%.2f' % line_total_client
        else:
            line_total = line_total_co
        entries[entry]['line_total'] = '%.2f' % line_total
    total = running_total_co - running_total_dev
    return (entries, running_total_co, running_total_dev, running_total_hours,
            total)


def get_active_kwarg(model, active=False, user=None):
    """
    Kwarg for "active" varies by type
    """
    kwargs = {}
    if model._meta.verbose_name == 'estimate':
        # Unaccepted invoices are "active"
        if active:
            kwargs['accepted_date'] = None
    elif model._meta.verbose_name == 'invoice':
        # Unpaid invoices are "active"
        if active:
            kwargs['last_payment_date'] = None
    elif model._meta.verbose_name == 'time':
        # Only staff can see all items
        if not user.is_staff:
            kwargs['user'] = user
        # Uninvoiced times are "active"
        kwargs['invoiced'] = not (active)
        # Estimated times are never "active"
        kwargs['estimate'] = None
    elif model._meta.verbose_name == 'user':
        # Use related model's active field
        kwargs['profile__active'] = active
    else:
        # All other models check active field
        kwargs['active'] = active
    return kwargs


def get_query(request, query):
    """
    """
    # Special handling for some query strings
    if query == 'paginated':
        paginated = request.GET.get('paginated')
        if paginated == u'false':
            return False
        else:
            return True
    elif query == 'search' and request.method == 'POST':
        return request.POST.get('search', '')
    elif query == 'values':
        values = request.GET.get('values')
        if values:
            values = values.split(' ')
        else:
            values = []
        values = [i.split(',') for i in values]
        return values
    else:  # Normal handling
        return request.GET.get(query, '')


def get_search_results(model, fields, search):
    context = {}
    query = []
    for field in fields:
        query.append(Q(**{field + '__icontains': search}))
    items = model.objects.filter(reduce(OR, query))
    context['items'] = items
    return context


def gravatar_url(email):
    """
    MD5 hash of email address for use with Gravatar
    """
    return settings.GRAVATAR_URL % md5(email.lower()).hexdigest()


def index_items(request, model, fields, context={}, order_by=None):
    """
    """
    page = get_query(request, 'page')
    paginated = get_query(request, 'paginated')
    search = get_query(request, 'search')

    # Search is easy
    if request.method == 'POST':
        if search == u'':  # Empty search returns none
            return {}
        else:
            return get_search_results(model, fields, search)

    # Not a search
    items = model.objects.all()

    # Reorder items
    if order_by:
        items = items.order_by(order_by)

    # Calculate cost per report
    if model._meta.verbose_name == 'report':
        for item in items:
            cost = item.gross - item.net
            item.cost = cost
            item.save()

    # Don't show items to anon
    if not request.user.is_authenticated:
        items = []

    # Paginate if paginated
    if paginated:
        items = paginate(items, page)

    context['items'] = items
    context['page'] = page
    context['paginated'] = paginated

    return context


def last_month():
    """
    Returns last day of last month
    """
    first = timezone.now().replace(day=1)
    return first - timezone.timedelta(days=1)


def paginate(items, page):
    """
    """
    paginator = Paginator(items, 10, orphans=5)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return items


def send_mail(request, subject, message, to):
    recipients = []
    sender = settings.DEFAULT_FROM_EMAIL
    recipients.append(to)

    # http://stackoverflow.com/a/28476681/185820
    html_message = render_to_string('cerberus-fluid.html',
                                    {'username': to,
                                     'message': message})
    try:
        django_send_mail(
            subject,
            message,
            sender,
            recipients,
            fail_silently=False,
            html_message=html_message)
        return True
    except SMTPSenderRefused:
        messages.add_message(request, messages.WARNING, 'SMTPSenderRefused!')
        return False


def url_name_from(verbose_name):
    """
    """
    url_name = {
        'client': 'client_index',
        'contact': 'contact_index',
        'estimate': 'estimate_index',
        'invoice': 'invoice_index',
        'note': 'note_index',
        'project': 'project_index',
        'report': 'report_index',
        'task': 'task_index',
        'time': 'entry_index',
    }
    return url_name[verbose_name]

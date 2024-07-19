from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, ProfileUpdateForm
from .models import User
from .models import User, Case, Document, Notification
from .forms import CaseForm
from django.contrib.auth.decorators import login_required
from django.db import migrations
from django.utils import timezone
from .forms import DocumentForm
from .models import Notification, Case
from .forms import CaseUpdateForm
from django.http import JsonResponse
from .models import Case, Notification, Document
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import UploadDocumentForm
from .models import Document, User

# CHATAPP IMPORT

from django.shortcuts import render, redirect
from .models import Message, Case
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.save()
            login(request, user)
            if user.role == 'client':
                return redirect('client_dashboard')
            elif user.role == 'lawyer':
                return redirect('lawyer_dashboard')
            elif user.role == 'judge':
                return redirect('judge_dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'client':
                return redirect('client_dashboard')
            elif user.role == 'lawyer':
                return redirect('lawyer_dashboard')
            elif user.role == 'judge':
                return redirect('judge_dashboard')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')


def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', user_id=request.user.id)
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

def client_dashboard(request):
    return render(request, 'client_dashboard.html')

def lawyer_dashboard(request):
    return render(request, 'lawyer_dashboard.html')

def judge_dashboard(request):
    return render(request, 'judge_dashboard.html')


def available_lawyers(request):
    lawyers = User.objects.filter(role='lawyer')
    return render(request, 'available_lawyers.html', {'lawyers': lawyers})


def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user_profile.html', {'user': user})



# the new code
def available_lawyers(request):
    lawyers = User.objects.filter(role='lawyer')
    return render(request, 'available_lawyers.html', {'lawyers': lawyers})

@login_required
def file_case(request, lawyer_id):
    lawyer = get_object_or_404(User, id=lawyer_id)
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.client = request.user
            case.lawyer = lawyer
            case.save()
            Notification.objects.create(
                case=case,
                recipient=lawyer,
                message=f'Your case "{case.title}" has been filed with {lawyer.full_name}.'
            )
            return redirect('client_dashboard')
    else:
        form = CaseForm()
    return render(request, 'file_case.html', {'form': form, 'lawyer': lawyer})
def client_dashboard(request):
    client_cases = Case.objects.filter(client=request.user)
    notifications = Notification.objects.filter(case__client=request.user)
    return render(request, 'client_dashboard.html', {
        'cases': client_cases,
        'notifications': notifications,
    })

def notifications(request):
    notifications = Notification.objects.filter(case__client=request.user)
    return render(request, 'notifications.html', {'notifications': notifications})

def case_history(request):
    client_cases = Case.objects.filter(client=request.user)
    return render(request, 'case_history.html', {'cases': client_cases})

def update_case(request, case_id):
    # Your view logic here
    return render(request, 'update_case.html')
def delete_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    case.delete()
    return redirect('case_history')


@login_required
def document_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            return redirect('document_history')
    else:
        form = DocumentForm()
    return render(request, 'document_upload.html', {'form': form})

@login_required
def document_history(request):
    documents = Document.objects.filter(uploaded_by=request.user)
    return render(request, 'document_history.html', {'documents': documents})

@login_required
def update_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, uploaded_by=request.user)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_history')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'document_update.html', {'form': form, 'document': document})

@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, uploaded_by=request.user)
    document.delete()
    return redirect('document_history')



def update_case_history(request, case_id):
    # Fetch the specific case based on the case_id and the current user
    case = get_object_or_404(Case, id=case_id, client=request.user)
    lawyer = case.lawyer

    if request.method == 'POST':
        form = CaseUpdateForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            return redirect('case_history')
    else:
        form = CaseUpdateForm(instance=case)

    context = {
        'form': form,
        'lawyer': lawyer,
    }

    return render(request, 'update_case_history.html', context)



@login_required
def get_dashboard_counts(request):
    user = request.user
    case_count = Case.objects.filter(client=user).count()
    notification_count = Notification.objects.filter(case__client=user).count()
    case_history_count = Case.objects.filter(client=user, status__in=['approved', 'rejected']).count()
    document_count = Document.objects.filter(case__client=user).count()
    document_history_count = Document.objects.filter(uploaded_by=user).count()

    return JsonResponse({
        'case_count': case_count,
        'notification_count': notification_count,
        'case_history_count': case_history_count,
        'document_count': document_count,
        'document_history_count': document_history_count
    })


# THE NEW ADDED LAWYER ACTION CODE

@login_required
def lawyer_dashboard(request):
    lawyer_cases = Case.objects.filter(lawyer=request.user)
    pending_cases = lawyer_cases.filter(status='pending')
    approved_cases = lawyer_cases.filter(status='approved')
    rejected_cases = lawyer_cases.filter(status='rejected')
    forwarded_cases = lawyer_cases.filter(status='forwarded')
    documents = Document.objects.filter(lawyer=request.user)

    return render(request, 'lawyer_dashboard.html', {
        'pending_cases': pending_cases,
        'approved_cases': approved_cases,
        'rejected_cases': rejected_cases,
        'forwarded_cases': forwarded_cases,
        'documents': documents,
    })

@login_required
def pending_cases(request):
    pending_cases = Case.objects.filter(lawyer=request.user, status='pending')
    return render(request, 'pending_cases.html', {'pending_cases': pending_cases})

@login_required
def approved_cases(request):
    approved_cases = Case.objects.filter(lawyer=request.user, status='approved')
    return render(request, 'approved_cases.html', {'approved_cases': approved_cases})

@login_required
def rejected_cases(request):
    rejected_cases = Case.objects.filter(lawyer=request.user, status='rejected')
    return render(request, 'rejected_cases.html', {'rejected_cases': rejected_cases})

@login_required
def forward_cases_to_judge(request):
    cases_to_forward = Case.objects.filter(lawyer=request.user, status='forwarded')
    return render(request, 'forward_cases.html', {'cases_to_forward': cases_to_forward})

@login_required
def forward_case_to_judge(request, case_id):
    case = get_object_or_404(Case, id=case_id, lawyer=request.user)
    case.status = 'forwarded_to_judge'
    case.save()
    Notification.objects.create(
        case=case,
        message=f'The case "{case.title}" has been forwarded to the judge by {request.user.full_name}.'
    )
    return redirect('forward_cases_to_judge')

@login_required
def forward_documents_to_judge(request):
    documents_to_forward = Document.objects.filter(lawyer=request.user, status='forwarded')
    return render(request, 'documents_to_judge.html', {'documents_to_forward': documents_to_forward})

@login_required
def forward_document_to_judge(request, document_id):
    document = get_object_or_404(Document, id=document_id, lawyer=request.user)
    document.status = 'forwarded_to_judge'
    document.save()
    Notification.objects.create(
        document=document,
        message=f'The document "{document.file.name}" has been forwarded to the judge by {request.user.full_name}.'
    )
    return redirect('forward_documents_to_judge')


# THE NEW ACTONS AGAIN

@login_required
def approve_case(request, case_id):
    case = get_object_or_404(Case, id=case_id, lawyer=request.user)
    case.status = 'approved'
    case.save()
    return redirect('pending_cases')

@login_required
def reject_case(request, case_id):
    case = get_object_or_404(Case, id=case_id, lawyer=request.user)
    case.status = 'rejected'
    case.save()
    return redirect('pending_cases')


# THE VIEW DOCUMENT CODE

@login_required
def view_documents(request):
    documents = Document.objects.filter(lawyer=request.user)
    return render(request, 'view_documents.html', {'documents': documents})



#THE CLIENTS UPLOAD DOCUMENT
@login_required
def upload_document(request):
    if request.method == 'POST':
        case_id = request.POST['case']
        lawyer_id = request.POST['lawyer']
        file = request.FILES['file']

        case = get_object_or_404(Case, id=case_id)
        lawyer = get_object_or_404(User, id=lawyer_id)

        document = Document.objects.create(
            case=case,
            lawyer=lawyer,
            file=file,
            status='pending'
        )

        # Create a notification for the lawyer
        Notification.objects.create(
            recipient=lawyer,
            message=f'A new document has been uploaded for the case: {case.title}'
        )

        return redirect('client_dashboard')

    pending_cases = Case.objects.filter(status='pending')
    assigned_lawyers = [case.lawyer for case in pending_cases]
    return render(request, 'upload_document.html', {'pending_cases': pending_cases, 'assigned_lawyers': assigned_lawyers})


# view case
@login_required
def view_case(request, case_id):
    case = get_object_or_404(Case, id=case_id, lawyer=request.user)
    documents = Document.objects.filter(case=case)
    return render(request, 'view_case.html', {'case': case, 'documents': documents})



# CORRECT UPLOAD DOCUMENT
@login_required
def upload_document(request):
    if request.method == 'POST':
        form = UploadDocumentForm(request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            document = form.save()
            # Notify the lawyer
            lawyer = document.lawyer
            # Send notification to the lawyer
            return redirect('client_dashboard')
    else:
        form = UploadDocumentForm(request.user)

    return render(request, 'upload_document.html', {'form': form})


#THE LAWYER DISPLAY DOCUMENT

@login_required
def lawyer_documents(request):
    documents = Document.objects.filter(lawyer=request.user)
    return render(request, 'documents.html', {'documents': documents})



# THE PDF VIEW
@login_required
def lawyer_documents(request):
    if request.user.role == 'lawyer':
        documents = Document.objects.filter(lawyer=request.user)
        pdf_documents = [doc for doc in documents if doc.file.name.endswith('.pdf')]
        doc_documents = [doc for doc in documents if doc.file.name.endswith('.doc') or doc.file.name.endswith('.docx')]
        image_documents = [doc for doc in documents if doc.file.name.endswith('.jpg') or doc.file.name.endswith('.jpeg') or doc.file.name.endswith('.png')]
        context = {
            'pdf_documents': pdf_documents,
            'doc_documents': doc_documents,
            'image_documents': image_documents
        }
        return render(request, 'documents.html', context)
    else:
        return HttpResponse('You are not authorized to view this page.', status=403)



    # RETRIVE AND DELETE CASE

def retrieve_case(request, case_id):
        case = get_object_or_404(Case, id=case_id)
        if case.status == 'rejected':
            case.status = 'pending'
            case.save()
            return redirect('rejected_cases')
        else:
            return redirect('rejected_cases')
"""def delete_case(request, case_id):
        case = get_object_or_404(Case, id=case_id)
        if case.status == 'rejected':
            case.delete()
            return redirect('rejected_cases')
        else:
            return redirect('rejected_cases')
"""
# DELETE APPROVE CASES
def delete_approved_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if case.status == 'approved':
        case.delete()
        return redirect('approved_cases')
    else:
        return redirect('approved_cases')


# CHATAPP FORUM
@login_required
def chat_view(request):
    return render(request, 'my_chatapp/chat.html')

@login_required
def chat(request):
    # Get the available lawyers
    lawyers = User.objects.filter(is_lawyer=True)

    # Check if there are any lawyers available
    if lawyers.exists():
        # Get the messages for the current user
        messages = Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).order_by('timestamp')

        # Get the cases for the current user
        if request.user.is_lawyer:
            cases = Case.objects.filter(lawyer=request.user)
        else:
            cases = Case.objects.filter(client=request.user)

        context = {
            'messages': messages,
            'cases': cases,
            'lawyers': lawyers
        }
        return render(request, 'chat.html', context)
    else:
        # Display a message or handle the situation in a different way
        return render(request, 'chat.html', {'no_lawyers_available': True})

# Other views remain the same
def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        recipient_id = request.POST.get('recipient_id')
        try:
            recipient = User.objects.get(id=recipient_id)
            new_message = Message.objects.create(
                sender=request.user,
                recipient=recipient,
                content=message,
                is_lawyer=request.user.is_lawyer
            )
            return JsonResponse({'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid recipient ID'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)
def delete_message(request):
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        try:
            message = Message.objects.get(id=message_id)
            if message.sender == request.user:
                message.delete()
                return JsonResponse({'success': 'Message deleted'})
            else:
                return JsonResponse({'error': 'You do not have permission to delete this message'}, status=403)
        except Message.DoesNotExist:
            return JsonResponse({'error': 'Message not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def mark_message(request):
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        try:
            message = Message.objects.get(id=message_id)
            if message.recipient == request.user:
                message.is_marked = True
                message.save()
                return JsonResponse({'success': 'Message marked'})
            else:
                return JsonResponse({'error': 'You do not have permission to mark this message'}, status=403)
        except Message.DoesNotExist:
            return JsonResponse({'error': 'Message not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)
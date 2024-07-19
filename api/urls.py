from django.urls import path
from . import views
from .views import case_history, update_case_history

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('client_dashboard/', views.client_dashboard, name='client_dashboard'),
    path('lawyer_dashboard/', views.lawyer_dashboard, name='lawyer_dashboard'),
    path('judge_dashboard/', views.judge_dashboard, name='judge_dashboard'),

    # the new added code

    path('available-lawyers/', views.available_lawyers, name='available_lawyers'),
    path('file-case/<int:lawyer_id>/', views.file_case, name='file_case'),
    path('notifications/', views.notifications, name='notifications'),
    path('case-history/', views.case_history, name='case_history'),
    path('update-case/<int:case_id>/', views.update_case, name='update_case'),
    path('delete-case/<int:case_id>/', views.delete_case, name='delete_case'),
    path('case-history/', views.case_history, name='case_history'),

    path('documents/upload/', views.document_upload, name='document_upload'),
    path('documents/<int:document_id>/delete/', views.delete_document, name='delete_document'),


    path('documents/upload/', views.document_upload, name='document_upload'),
    path('documents/history/', views.document_history, name='document_history'),
    path('documents/<int:document_id>/update/', views.update_document, name='update_document'),
    path('documents/<int:document_id>/delete/', views.delete_document, name='delete_document'),
    path('update-case/<int:case_id>/', views.update_case, name='update_case'),
    path('update/<int:case_id>/', update_case_history, name='update_case_history'),
    path('get-dashboard-counts/', views.get_dashboard_counts, name='get_dashboard_counts'),



 # Lawyer-related URL patterns
    path('lawyer/dashboard/', views.lawyer_dashboard, name='lawyer_dashboard'),
    path('lawyer/pending-cases/', views.pending_cases, name='pending_cases'),
    path('lawyer/approved-cases/', views.approved_cases, name='approved_cases'),
    path('lawyer/rejected-cases/', views.rejected_cases, name='rejected_cases'),
    path('lawyer/forward-cases-to-judge/', views.forward_cases_to_judge, name='forward_cases_to_judge'),
    path('lawyer/forward-case-to-judge/<int:case_id>/', views.forward_case_to_judge, name='forward_case_to_judge'),
    path('lawyer/forward-documents-to-judge/', views.forward_documents_to_judge, name='forward_documents_to_judge'),
    path('lawyer/forward-document-to-judge/<int:document_id>/', views.forward_document_to_judge, name='forward_document_to_judge'),

    # THE PENDING AND APPROVE URLS
    path('lawyer/approve-case/<int:case_id>/', views.approve_case, name='approve_case'),
    path('lawyer/reject-case/<int:case_id>/', views.reject_case, name='reject_case'),

    # THE VIEW DOCUMENTS
    path('lawyer/view-documents/', views.view_documents, name='view_documents'),

    #UPLOAD DOCUMENT
    path('upload-document/', views.upload_document, name='upload_document'),
    path('approve-case/<int:case_id>/', views.approve_case, name='approve_case'),

    path('case/<int:case_id>/', views.view_case, name='view_case'),

    # correct upload document
    path('client/upload-document/', views.upload_document, name='upload_document'),


    #LAWYER DISPLAY DOCUMENTS
    path('lawyer/documents/', views.lawyer_documents, name='lawyer_documents'),

    # RETRIVE CASE AND DELETE CASE
    path('retrieve_case/<int:case_id>/', views.retrieve_case, name='retrieve_case'),
    path('delete_case/<int:case_id>/', views.delete_case, name='delete_case'),
    # DELETE APPROVE CASE
    path('delete_approved_case/<int:case_id>/', views.delete_approved_case, name='delete_approved_case'),

    # CHATAPP CODE URLS
    path('chat/', views.chat_view, name='chat'),
    path('chat/', views.chat, name='chat'),
    path('send_message/', views.send_message, name='send_message'),
    path('delete_message/', views.delete_message, name='delete_message'),
    path('mark_message/', views.mark_message, name='mark_message'),
]







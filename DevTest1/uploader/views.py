import pandas as pd
from django.shortcuts import render
from .forms import UploadFileForm
from django.core.mail import send_mail
from django.conf import settings

def upload_file(request):
    success_message = None
    error_message = None
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Process the uploaded file
                file = request.FILES['file']
                df = pd.read_excel(file)
                
                # Generate summary
                summary = df.groupby(['Cust State', 'Cust Pin'])['DPD'].count().reset_index()
                
                # Send email
                email_subject = 'Python Assignment - Ashish Gupta'
                email_body = summary.to_string()
                send_mail(email_subject, email_body, 'ashu170800@gmail.com', ['tech@themedius.ai', 'yash@themedius.ai', 'ashishguptaji21@gmail.com'], fail_silently=False)
                
                success_message = 'File uploaded and email sent successfully!✌️'
            except Exception as e:
                print(e)
                error_message = 'Failed the process.'
        else:
            error_message = 'Invalid file upload.'

    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form, 'success_message': success_message, 'error_message': error_message})

from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

def learning_journal(request):
    return render(request, 'learning_journal.html')

def matkul(request):
    return render(request, 'matkul.html')

def plagiarism(request):
    return render(request, 'plagiarism.html')

def form_mahasiswa(request):
    return render(request, 'form_mahasiswa.html')
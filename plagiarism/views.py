from django.shortcuts import redirect, render

from plagiarism.models import MataKuliah, Semester

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

def learning_journal(request):
    return render(request, 'learning_journal.html')

def matkul(request):
    if request.method == "GET":
        context= {
            'matkul':MataKuliah.objects.all()
        }
        
        return render(request, 'matkul.html',context)
    elif request.method == "POST":
        data = {
            'nama':request.POST.get("matkul"),
            'semester':request.POST.get("semester"),
        }

        MataKuliah.objects.update_or_create(
                        nama = request.POST.get("matkul"),
                        defaults=data
                    )
        return redirect('matkul')
def matkul_delete(request,id):
    MataKuliah.objects.filter(id=id).delete()
    return redirect('matkul')

def plagiarism(request):
    return render(request, 'plagiarism.html')

def form_mahasiswa(request):
    return render(request, 'form_mahasiswa.html')
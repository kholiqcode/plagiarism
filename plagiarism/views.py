from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
import pandas as pd
from core.preprocessing import PreProcessing

from plagiarism.models import LearningJurnal, MataKuliah, Semester

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

def learning_journal(request):
    if request.method == "GET":
        context= {
            'journal':LearningJurnal.objects.all()
        }
    return render(request, 'learning_journal.html',context)

def detail_journal(request,id):
    if request.method == "GET":
        context= {
            'journal':LearningJurnal.objects.filter(id=id).first()
        }
        return render(request, 'detail_journal.html',context)

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
    if request.method == "GET":
        context= {
            'matkul':MataKuliah.objects.all()
        }
        return render(request, 'form_mahasiswa.html',context)
    elif request.method == "POST":
        data = {
            'email':request.POST.get("email"),
            'nama':request.POST.get("nama"),
            'nim':request.POST.get("nim"),
            'golongan':request.POST.get("golongan"),
            'semester':request.POST.get("semester"),
            'matkul':request.POST.get("matkul"),
            'minggu':request.POST.get("minggu"),
            'tanggal':datetime.strptime(str(request.POST.get("tanggal")), "%Y-%m-%d"),
            'topik':request.POST.get("topik"),
            'pembahasan':request.POST.get("pembahasan"),
        }
        df = pd.DataFrame([data.values()],columns=data.keys())
        preprocessing = PreProcessing()
        normalization = df['pembahasan'].apply(lambda x : preprocessing.callback(x))
        df = pd.concat([df,normalization], axis=1, join='inner')
        # df.to_csv('data.csv')
        for index, row in df.iterrows():
            matkul = MataKuliah.objects.filter(id=row['matkul']).first()
            model = LearningJurnal()
            model.email = row['email']
            model.nama = row['nama']
            model.nim = row['nim']
            model.semester = row['semester']
            model.golongan = row['golongan']
            model.matkul = matkul
            model.minggu = row['minggu']
            model.tanggal_perkuliahan = row['tanggal']
            model.topik = row['topik']
            model.pembahasan = row['pembahasan']
            model.cleaning = row['cleaning']
            model.casefolding = row['casefolding']
            model.tokenizing = row['tokenizing']
            model.normalisasi = row['normalisasi']
            model.stopword = row['stopword']
            model.steeming = row['steeming']
            model.cleaned = row['cleaned']
            model.save()
        return redirect('learning_journal')

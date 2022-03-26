from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
import pandas as pd
from core.preprocessing import PreProcessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Count

from plagiarism.models import LearningJurnal, MataKuliah, Semester

def cosine_sklearn(docs):
    # Initialize an instance of tf-idf Vectorizer
    tfidf_vectorizer = TfidfVectorizer(norm=None)

    # Generate the tf-idf vectors for the corpus
    tfidf_matrix = tfidf_vectorizer.fit_transform(docs)
    
    cosine_sim = cosine_similarity(tfidf_matrix)
    return cosine_sim*100

# Create your views here.
def dashboard(request):
    context = {
        'total_journal':LearningJurnal.objects.count(),
        'total_mahasiswa':LearningJurnal.objects.values('nim').annotate(count_nim=Count('nim')).count(),
        'total_matkul':MataKuliah.objects.count(),
    }
    return render(request, 'dashboard.html',context)

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
    journals = LearningJurnal.objects
    if request.GET.get("semester") is not None:
        semester = request.GET.get("semester")
        journals=journals.filter(semester=semester)
    
    df = pd.DataFrame(list(journals.values()))
    cosine = cosine_sklearn(df['cleaned'])
    plagiarism_list = []
    for i,v in df.iterrows():
        # plagiarism_list[v['nim']] = []
        for i2,v2 in df.iterrows():
            exists = list(filter(lambda x: (x.get('nim_q1') == v['nim']) & (x.get('nim_q2') == v2['nim']) | (x.get('nim_q1') == v2['nim']) & (x.get('nim_q2') == v['nim']), plagiarism_list))
            if len(exists) == 0 and v['nim'] != v2['nim']:
                data = {
                    'nim_q1':v['nim'],
                    'nim_q2':v2['nim'],
                    'score': round(cosine[i][i2],2)
                }
                plagiarism_list.append(data)
    context= {
            'plagiarism' : list(plagiarism_list)
        }
    return render(request, 'plagiarism.html',context)

def test(request):
    journals = LearningJurnal.objects.all()
    df = pd.DataFrame(list(journals.values()))
    cosine = cosine_sklearn(df['cleaned'])
    plagiarism_list = []
    for i,v in df.iterrows():
        # plagiarism_list[v['nim']] = []
        for i2,v2 in df.iterrows():
            exists = list(filter(lambda x: (x.get('nim_q1') == v['nim']) or (x.get('nim_q2') == v2['nim']), plagiarism_list))
            if len(exists) == 0:
                data = {
                    'nim_q1':v['nim'],
                    'nim_q2':v2['nim'],
                    'score': cosine[i2]
                }
                plagiarism_list.append(data)
    
    return HttpResponse(cosine)

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

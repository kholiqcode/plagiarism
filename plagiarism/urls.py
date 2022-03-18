from django.urls import path

from plagiarism.views import dashboard, form_mahasiswa, learning_journal, matkul, plagiarism


urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('learning-journal', learning_journal, name="learning_journal"),
    path('matkul', matkul, name="matkul"),
    path('plagiarism', plagiarism, name="plagiarism"),
    path('form-mahasiswa', form_mahasiswa, name="form_mahasiswa"),
]
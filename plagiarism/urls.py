from django.urls import path

from plagiarism.views import dashboard, detail_journal, form_mahasiswa, learning_journal, matkul, matkul_delete, plagiarism, test


urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('learning-journal', learning_journal, name="learning_journal"),
    path('detail-journal/<str:id>', detail_journal, name="detail_journal"),
    path('matkul', matkul, name="matkul"),
    path('matkul/delete/<str:id>', matkul_delete, name="matkul_delete"),
    path('plagiarism', plagiarism, name="plagiarism"),
    path('form-mahasiswa', form_mahasiswa, name="form_mahasiswa"),
    path('test', test, name="test"),
]
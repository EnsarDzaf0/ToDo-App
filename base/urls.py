from django.urls import path #kreirati url fajl
from .views import TaskDetail, TaskList, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage
#imporatti path i views generalno
from django.contrib.auth.views import LogoutView

urlpatterns =[ 
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path ('register/', RegisterPage.as_view(), name='register'),
    
    path('', TaskList.as_view(), name='tasks'), 
    #ne moze skontati class tkd moras metodu as view pozvati
    path('task/<int:pk>', TaskDetail.as_view(), name='task'),
    #view trazi id koji smo poslali
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>', DeleteView.as_view(), name='task-delete'),
]

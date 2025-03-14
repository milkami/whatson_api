from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('teams/', TeamsView.as_view(), name='team'),
    path('user/<int:pk>/', UserView.as_view()),
    path('static/bpp/questions', StaticBppQuestionsView.as_view(), name='static_bpp_questions'),
    path('static/ed/questions', StaticEdQuestionsView.as_view(), name='static_bpp_questions'),
    path('user/<int:pk>/<int:team_pk>/static_report', TeamReportView.as_view(), name='team_report'),
    path('user/<int:pk>/<int:team_pk>/static_answers', TeamAnswersView.as_view(), name='team_answers'),
]

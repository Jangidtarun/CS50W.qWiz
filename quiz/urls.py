from django.urls import path
from . import views

urlpatterns = [
    # Home and Main Pages
    path('', views.index, name='index'),

    # Authentication
    path("login/", views.login_user, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path('send-otp/<str:email_id>/', views.send_otp, name='send_otp'),
    path('verify-otp/<str:email_id>/<int:otp>/', views.verify_otp, name='verify_otp'),
    path('sendresetlinkpage/', views.send_reset_link, name='sendresetlink'),
    path('reset-password/<uid>/<token>/', views.reset_password, name='reset_password'),

    # Profile Management
    path('profile/', views.profile, name='profile'),
    path('remove-photo/', views.remove_photo, name='remove-photo'),
    path('view-profile/<int:pid>/', views.view_profile, name='view_profile'),
    path('update-user/', views.update_user, name='update_user'),
    path('delete_user/', views.delete_user, name='delete_user'),

    # Quiz Management
    path('create/', views.create, name='create'),
    path('take/', views.take_quiz, name='take'),
    path('quiz/<int:qid>/', views.take_quiz_helper, name='take_quiz'),
    path('submit/', views.quiz_submit, name='submit'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('delete/<int:pk>/', views.delete_question, name='delete'),
    path('question/<int:pk>/', views.question, name='get-question'),
    path('results/<int:rid>/', views.showresults, name='results'),
    path('instant-quiz/', views.gotoinstantquiz, name='goto_instant_quiz'),

    # Topics and Comments
    path('topics/', views.topics, name='topics'),
    path('delete-topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    path('topic/<str:topicname>/', views.question_with_topic, name='qwtopic'),
    path('make-comment/', views.make_comment, name='make_comment'),
    path('delete-comment/<int:cid>/', views.delete_comment, name='deletec'),
    path('update_vote/<int:qid>/', views.update_vote, name='updatevote'),

    # Search
    path('search/', views.search, name='search'),
]

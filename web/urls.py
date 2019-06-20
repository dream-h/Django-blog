from django.urls import path
from .views import home, account, article_op

app_name = 'web'
urlpatterns = [
    path('all/<int:article_type_id>', home.index, name='index'),
    path('', home.index, name='home'),

    path('login/', account.login, name='login'),
    path('check_code/', account.check_code, name='check_code'),
    path('logout/', account.logout, name='logout'),
    path('register/', account.register, name='register'),

    path('article-<int:article_type_id>-<int:category_id>/', home.user_article_list, name='article'),
    path('<str:site>/', home.user_blog, name='user_blog'),
    path('<str:site>/filter/<str:condition>/<nid>/', home.article_filter, name='article_filter'),
    path('<str:site>/add_article/', article_op.add_article, name='add_article'),
    path('<str:site>/edit_article/<int:nid>/', article_op.edit_article, name='edit_article'),
    path('<str:site>/del_article/<int:nid>/', article_op.del_article, name='del_article'),
    path('<str:site>/article_detail/<int:nid>/', article_op.article_detail, name='article_detail'),
]
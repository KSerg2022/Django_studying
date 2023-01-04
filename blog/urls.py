from django.urls import path, re_path

from . import views


app_name = 'blog'

urlpatterns = [
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'^user/settings/$', views.settings, name='settings'),

    path('', views.index, name='index'),
    re_path(r'^add/post/$', views.add_post, name='add_post'),
    re_path(r'^user/posts/$', views.get_user_posts, name='get_user_posts'),
    path('user/posts/published/<published>', views.get_user_posts, name='get_user_posts_published'),
    path('user/posts/draft/<draft>', views.get_user_posts, name='get_user_posts_draft'),
    re_path(r'^user/post/edit/(?P<post_id>[\d]+)', views.edit_post, name='edit_post'),
    re_path(r'^user/post/delete/(?P<post_id>[\d]+)', views.delete_post, name='delete_post'),
    path('user/post/delete/<int:post_id>/', views.delete_post, name='sure_delete_post'),

    re_path(r'^posts/$', views.PostListView.as_view(), name='posts'),
    re_path(r'^posts/draft/$', views.PostDraftListView.as_view(), name='draft_post'),
    path('posts/<tag>', views.post_list_for_, name='post_list_for_tag'),
    path('posts/author/<author>', views.post_list_for_, name='post_list_for_author'),

    path('posts/user/<user>/<tag>', views.user_posts_for_, name='user_posts_for_tag'),

    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail,  name='post_detail'),


]

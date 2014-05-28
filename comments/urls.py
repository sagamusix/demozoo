from django.conf.urls import url

from comments.views import AddProductionCommentView, EditProductionCommentView, delete_production_comment

urlpatterns = [
	url(r'^productions/(\d+)/comments/new/$', AddProductionCommentView.as_view(), name='add_production_comment'),
	url(r'^productions/(\d+)/comments/(\d+)/edit/$', EditProductionCommentView.as_view(), name='edit_production_comment'),
	url(r'^productions/(\d+)/comments/(\d+)/delete/$', delete_production_comment, name='delete_production_comment'),
]

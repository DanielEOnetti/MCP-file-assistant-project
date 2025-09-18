from django.urls import path
from tools.views import ToolsManifestView, ReadFileView, WriteFileView, ListFilesView

urlpatterns = [
    path('tools/manifest', ToolsManifestView.as_view(), name='tools_manifest'),
    path('tools/read_file', ReadFileView.as_view(), name='read_file'),
    path('tools/write_file', WriteFileView.as_view(), name='write_file'),
    path('tools/list_files', ListFilesView.as_view(), name='list_files'),
]
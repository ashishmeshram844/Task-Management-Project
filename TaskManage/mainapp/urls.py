from django.urls import path,include
from mainapp.views import *


urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('<int:task_id>/',IndexView.as_view(),name='update_task'),
    path('history/<int:task_id>/',TaskHistory,name='history'),
    path('delete_task/<int:task_id>/',DeleteTask,name='delete_task'),
    path('subtasks/<int:task_id>/',SubTasks.as_view(),name='subtasks'),
    path('subtask_update/<int:subtask_id>/',SubTaskUpdate.as_view(),name='subtask_update'),
    path('save_subtask_work/<int:subtask_id>/',SaveSubtaskWork,name='save_subtask_work'),
    path('delete_subtask_work/<int:sub_work_id>/',delete_subtask_work,name='delete_subtask_work'),
    path('delete_subtask/<int:subtask_id>/',delete_subtask,name='delete_subtask'),
    path('save_milestone',save_milestone,name='save_milestone'),
    path('save_sprint',save_sprint,name='save_sprint'),
    path('download_excel_data',download_excel_data,name='download_excel_data'),



    path('download_excel',DownloadExcel.as_view(),name='download_excel'),
    
]



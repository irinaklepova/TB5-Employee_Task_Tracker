from trackers.apps import TrackersConfig
from rest_framework.routers import DefaultRouter
from django.urls import path
from trackers.views import (
    EmployeeViewSet,
    TaskListAPIView,
    TaskRetrieveAPIView,
    TaskUpdateAPIView,
    TaskDeleteAPIView,
    TaskCreateAPIView,
    EmployeeTrackAPIView,
    ImportantTasksForEmployeesAPIView,
)

app_name = TrackersConfig.name

router = DefaultRouter()
router.register(r"employees", EmployeeViewSet, basename="employees")

urlpatterns = [
                  path("task/task_list/", TaskListAPIView.as_view(), name="task_list"),
                  path("task/retrieve/<int:pk>/", TaskRetrieveAPIView.as_view(), name="task_retrieve"),
                  path("task/create/", TaskCreateAPIView.as_view(), name="task_create"),
                  path("task/update/<int:pk>/", TaskUpdateAPIView.as_view(), name="task_update"),
                  path("task/delete/<int:pk>/", TaskDeleteAPIView.as_view(), name="task_delete"),
                  path("employee_track/employee_track_list/", EmployeeTrackAPIView.as_view(),
                       name="employee_track_list"),
                  path(
                      "important_tasks/important_tasks_list/",
                      ImportantTasksForEmployeesAPIView.as_view(),
                      name="important_tasks_list"
                  ),
              ] + router.urls

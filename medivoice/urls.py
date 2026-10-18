
from django.urls import path

from medivoice.views import RegistrationView
from medivoice.views import ComplaintListCreateView,ComplaintRetrieveUpdateDeleteView
from medivoice.views import ComplaintUnresolvedView,ComplaintCountView,ComplaintPriorityView
from medivoice.views import ComplaintFilterView,ComplaintSearchView

urlpatterns = [

    # route for registration view
    path("register/",RegistrationView.as_view()),

    # route for complaint list,create view
    path("complaint/",ComplaintListCreateView.as_view()),

    # route for complaint retrieve,update,delete view
    path("complaint/<int:pk>/",ComplaintRetrieveUpdateDeleteView.as_view()),

    # route for unresolved complaints view
    path("complaint/unresolved/",ComplaintUnresolvedView.as_view()),

    # route for user complaint count
    path("complaint/count/",ComplaintCountView.as_view()),

    # route for priority complaints view
    path("complaint/priority/",ComplaintPriorityView.as_view()),

    # route for filtering
    path("complaint/filter/",ComplaintFilterView.as_view()),

    # route for searching
    path("complaint/search/",ComplaintSearchView.as_view()),
]
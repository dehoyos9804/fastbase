# -*- coding: utf-8 -*-
from extensions.url_manager import Url
from apps.home.controller.home_controller import home_router

urlpatterns = [Url(home_router, endpoint='', tags=['home'])]

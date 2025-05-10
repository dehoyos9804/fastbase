# -*- coding: utf-8 -*-
from typing import Any
from typing import Dict
from typing import Optional
from fastapi.responses import ORJSONResponse
from fastapi import status


class Rest:
    """
    """
    @staticmethod
    def response(
        status_http: int = status.HTTP_200_OK,
        message: str = None,
        data: Any = None,
        errors: Optional[Dict[str, Any]] = None
    ):
        if not message:
            message = ''

        content = {
            'status': status_http,
            'message': message
        }

        if data:
            content['data'] = data

        if errors:
            content['errors'] = errors

        return ORJSONResponse(
            status_code=status_http,
            content=content
        )

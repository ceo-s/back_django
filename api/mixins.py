from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class FilteredSearch:

    # TODO объединить валидацию коуча в один метод

    # def filter2(self, request: Request):
    #     params = request.query_params.dict()
    #     if params["coach"]:
    #         params["coach"] = request.user
    #     if params["chained"]:
    #         del params["chained"]
    #     pass

    @action(methods=["get"], detail=False, url_name="filter")
    def filter(self, request: Request, *args, **kwargs):
        queryset = self.get_queryset()
        params = request.query_params.dict()
        if getattr(queryset.model, "coach", False):
            params["coach"] = request.user

        filtered_queryset = queryset.filter(**params)
        serializer = self.get_serializer(filtered_queryset, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_200_OK, headers=headers, data=serializer.data)

    @action(methods=["get"], detail=False, url_name="chain_filter")
    def chain_filter(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        if getattr(queryset.model, "coach", False):
            queryset = queryset.filter(**{"coach": request.user.id})

        params = request.query_params.dict()
        for key in params:
            param_list = params[key].split(",")
            for item in param_list:
                queryset = queryset.filter(**{key: item})

        serializer = self.get_serializer(queryset, many=True)
        headers = self.get_success_headers(serializer)
        return Response(status=status.HTTP_200_OK, headers=headers, data=serializer.data)

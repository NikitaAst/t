import logging
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .query import AdvertQuery
from .serializers import AdvertSerializer

logger = logging.getLogger('advert')


class AdvertPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class AdvertListView(APIView):
    pagination_class = AdvertPagination
    filterset_fields = ['title', 'description', 'views', 'category__name', 'city__name', 'created_at', 'uuids']
    ordering_fields = ['title', 'description', 'views', 'category__name', 'city__name', 'created_at', 'uuid']

    def get(self, request, format=None):
        start_time = time.time()
        logger.debug('Starting processing request')

        query = AdvertQuery()

        for key, value in request.query_params.items():
            if key in self.filterset_fields:
                query = query.filter(**{key: value})

        ordering = request.query_params.get('ordering', None)
        if ordering:
            query = query.order_by(ordering)

        pagination_start_time = time.time()
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', self.pagination_class.page_size))
        query = query.with_pagination(page, page_size)
        results, total_count = query.fetch_paginated()
        pagination_end_time = time.time()
        logger.debug(f'Query took {pagination_end_time - pagination_start_time:.4f} seconds')

        serializer = AdvertSerializer(results, many=True)
        response = Response({
            'count': total_count,
            'results': serializer.data
        })

        end_time = time.time()
        logger.debug(f'Total request processing took {end_time - start_time:.4f} seconds')

        return response

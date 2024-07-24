from django.db import connection
from uuid import UUID

DEFAULT_PAGE_SIZE = 100
MAX_FETCH = 5_000_000


COLUMN_MAPPING = {
    'category__name': 'category_name',
    'city__name': 'city_name'
}


class AdvertQuery:

    def __init__(self):
        self.__frozen = False
        self.__page = None
        self.__take = None
        self.__page_size = DEFAULT_PAGE_SIZE

        self.__filters = {}
        self.__ordering = []

    def _exec_query(self, query: str, params: dict):
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    def _ensure_not_frozen(self):
        if self.__frozen:
            raise ValueError("Query is frozen")

    def with_pagination(self, page: int, page_size: int = DEFAULT_PAGE_SIZE) -> 'AdvertQuery':
        self._ensure_not_frozen()
        if self.__take is not None:
            raise ValueError("Cannot set pagination with take already set")

        self.__page = page
        self.__page_size = page_size
        return self

    def take(self, count: int) -> 'AdvertQuery':
        self._ensure_not_frozen()
        if self.__page is not None:
            raise ValueError("Cannot set take with pagination already set")
        self.__take = count
        return self

    def filter(self, **kwargs) -> 'AdvertQuery':
        self._ensure_not_frozen()
        for key, value in kwargs.items():
            if key == 'uuids':
                uuids = [UUID(u) for u in value.split(',')]
                self.__filters[key] = uuids
                if len(uuids) == 1:
                    self._increment_views(uuids[0])
            else:
                self.__filters[key] = value
        return self

    def _increment_views(self, uuid: UUID):
        with connection.cursor() as cursor:
            cursor.execute("SELECT increment_advert_views(%s)", [uuid])

    def order_by(self, *args) -> 'AdvertQuery':
        self._ensure_not_frozen()
        ordering_map = {}

        for arg in args:
            if arg.startswith('-'):
                column = arg[1:]
                direction = 'DESC'
            else:
                column = arg
                direction = 'ASC'

            if column in COLUMN_MAPPING:
                ordering_map[COLUMN_MAPPING[column]] = direction
            else:
                ordering_map[f"fa.{column}"] = direction

        self.__ordering = [f"{column} {direction}" for column, direction in ordering_map.items()]
        return self

    def _determine_limit_and_offset(self) -> tuple[int, int]:
        if self.__take is not None:
            return self.__take, 0

        if self.__page is None:
            return MAX_FETCH, 0

        return self.__page_size, (self.__page - 1) * self.__page_size

    def fetch_paginated(self) -> tuple[list[dict], int]:
        self.__frozen = True
        limit, offset = self._determine_limit_and_offset()

        filter_clauses_inner = []
        filter_clauses_outer = []
        params = {}

        for key, value in self.__filters.items():
            if key == 'uuids':
                filter_clauses_outer.append(f"fa.uuid = ANY(%({key})s::uuid[])")
                params[key] = value
            elif key in COLUMN_MAPPING:
                filter_clauses_outer.append(f"{COLUMN_MAPPING[key]} ILIKE %({key})s")
                params[key] = f"%{value}%"  # For contains match
            elif key in ['title', 'description']:
                filter_clauses_inner.append(f"a.{key} ILIKE %({key})s")
                params[key] = f"%{value}%"  # For contains match
            else:
                filter_clauses_inner.append(f"a.{key} = %({key})s")
                params[key] = value

        filter_sql_inner = " AND ".join(filter_clauses_inner)
        if filter_sql_inner:
            filter_sql_inner = f"WHERE {filter_sql_inner}"

        filter_sql_outer = " AND ".join(filter_clauses_outer)
        if filter_sql_outer:
            filter_sql_outer = f"WHERE {filter_sql_outer}"

        order_sql = ", ".join(self.__ordering) if self.__ordering else "fa.created_at DESC"

        query = f"""
        WITH filtered_adverts AS (
            SELECT a.*, c.name AS category_name, ci.name AS city_name
            FROM advert_advert a
            LEFT JOIN advert_category c ON a.category_id = c.uuid
            LEFT JOIN advert_city ci ON a.city_id = ci.uuid
            {filter_sql_inner}
        )
        SELECT fa.*
        FROM filtered_adverts fa
        {filter_sql_outer}
        ORDER BY {order_sql}
        LIMIT {limit} OFFSET {offset}
        """

        count_query = f"""
        WITH filtered_adverts AS (
            SELECT a.*, c.name AS category_name, ci.name AS city_name
            FROM advert_advert a
            LEFT JOIN advert_category c ON a.category_id = c.uuid
            LEFT JOIN advert_city ci ON a.city_id = ci.uuid
            {filter_sql_inner}
        )
        SELECT COUNT(*)
        FROM filtered_adverts fa
        {filter_sql_outer}
        """

        results = self._exec_query(query, params)
        total_count = self._exec_query(count_query, params)[0]['count']

        return results, total_count

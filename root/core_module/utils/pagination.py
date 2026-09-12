from django.db.models import Q

def parse_pagination_params(request, default_sort='id', default_direction='desc'):
    """Parse pagination, sorting and search params from request."""
    search = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort_by', default_sort)
    sort_direction = request.GET.get('sort_direction', default_direction)
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 10
        if page_size > 100:
            page_size = 100
    except (ValueError, TypeError):
        page, page_size = 1, 10
    return search, sort_by, sort_direction, page, page_size

def apply_sorting(queryset, allowed_sort, sort_by, sort_direction, default='id'):
    """Apply safe sorting to queryset."""
    sort_field = allowed_sort.get(sort_by, default)
    if sort_direction not in ['asc', 'desc']:
        sort_direction = 'desc'
    ordering = sort_field if sort_direction == 'asc' else f'-{sort_field}'
    try:
        return queryset.order_by(ordering)
    except Exception:
        return queryset.order_by(f'-{default}')

def apply_search(queryset, search_fields, search):
    """Apply search across fields if search provided."""
    if not search or not search_fields:
        return queryset
    q = Q()
    for field in search_fields:
        q |= Q(**{f"{field}__icontains": search})
    return queryset.filter(q)

def paginate_queryset(queryset, page, page_size):
    """Paginate queryset and return page_qs, total, total_pages."""
    total = queryset.count()
    start = (page - 1) * page_size
    end = start + page_size
    page_qs = queryset[start:end]
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 1
    return page_qs, total, total_pages

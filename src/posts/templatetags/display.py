# coding: utf-8
from django import template


register = template.Library()


@register.filter
def limited_page_range(num_pages, current_page_number):
    limit = 5
    page_range = [current_page_number]

    def add_pages(page_range):
        start_page = page_range[0]
        end_page = page_range[-1]

        if len(page_range) == limit or (start_page == 1 and end_page == num_pages):
            return page_range
        elif ((current_page_number - start_page <= end_page - current_page_number) or end_page == num_pages) \
            and start_page != 1:
            page_range.insert(0, start_page - 1)
        else:
            page_range.append(end_page + 1)
        return add_pages(page_range)

    return add_pages(page_range)

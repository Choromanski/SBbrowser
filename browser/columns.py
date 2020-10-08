# SPDX-License-Identifier: AGPL-3.0-or-later
import datetime
import django_tables2 as tables

from django.utils.html import format_html
from django.db.models import F, QuerySet
from django.utils.html import escape


class UsernameColumn(tables.Column):
    def render(self, value: str) -> str:
        return format_html(f'<textarea class="form-control" name="Username" readonly>{escape(value)}</textarea>'
                           f'<button onclick="copyToClipboard(\'{escape(value)}\');">✂</button>'
                           f'<a href="/username/{escape(value)}/">🔗</a>')


class LengthColumn(tables.Column):
    def render(self, value: float) -> datetime.timedelta:
        return datetime.timedelta(seconds=value)

    def order(self, qs: QuerySet, is_descending: bool) -> (QuerySet, bool):
        qs = qs.annotate(
            length=F("endtime") - F("starttime")
        ).order_by(("-" if is_descending else "") + "length")
        return qs, True

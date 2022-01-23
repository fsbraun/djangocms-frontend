import copy

from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import select_template
from django.utils.functional import lazy
from django.utils.safestring import mark_safe

from djangocms_frontend import settings


def insert_fields(fieldsets, new_fields, block=None, position=-1, blockname=None):
    """
    creates a copy of fieldsets inserting the new fields either in the indexed block at the position,
    or - if no block is given - at the end
    """
    if block is None:
        fs = (
            fieldsets[:position]
            + [
                (
                    blockname,
                    {
                        "classes": ("collapse",),
                        "fields": new_fields,
                    },
                )
            ]
            + (fieldsets[position:] if position != -1 else [])
        )
        return fs
    modify = fieldsets[block]
    fields = modify[1]["fields"]
    modify[1]["fields"] = (
        fields[:position]
        + new_fields
        + (fields[: position + 1] if position != -1 else [])
    )
    fs = fieldsets[:block] + [modify] + (fieldsets[block + 1 :] if block != -1 else [])
    return fs


def get_template_path(prefix, template, name):
    return f"djangocms_frontend/{settings.framework}/{prefix}/{template}/{name}.html"


def get_plugin_template(instance, prefix, name, templates):
    template = getattr(instance, "template", templates[0][0])
    template_path = get_template_path(prefix, template, name)

    try:
        select_template([template_path])
    except TemplateDoesNotExist:
        # TODO render a warning inside the template
        template_path = get_template_path(prefix, "default", name)

    return template_path


# use mark_safe_lazy to delay the translation when using mark_safe
# otherwise they will not be added to /locale/
# https://docs.djangoproject.com/en/1.11/topics/i18n/translation/#other-uses-of-lazy-in-delayed-translations
mark_safe_lazy = lazy(mark_safe, str)
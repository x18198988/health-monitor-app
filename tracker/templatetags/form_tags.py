from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    attrs = field.field.widget.attrs
    attrs['class'] = css_class

    # Set example placeholders if field name matches
    if field.name == "steps":
        attrs["placeholder"] = "e.g., 8000"
    elif field.name == "sleep_hours":
        attrs["placeholder"] = "e.g., 7.5"
    elif field.name == "calories":
        attrs["placeholder"] = "e.g., 2200"
    elif field.name == "date":
        attrs["placeholder"] = "YYYY-MM-DD"

    return field.as_widget(attrs=attrs)

from demo.widget.forms import TestForm
from demo.widget.models import NonRequired, Required


class RequiredForm(TestForm):
    class Meta(TestForm.Meta):
        model = Required


class NonRequiredForm(TestForm):
    class Meta(TestForm.Meta):
        model = NonRequired

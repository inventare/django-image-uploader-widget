from tests.app.widget.forms import TestForm
from tests.app.widget.models import NonRequired, Required


class RequiredForm(TestForm):
    class Meta(TestForm.Meta):
        model = Required


class NonRequiredForm(TestForm):
    class Meta(TestForm.Meta):
        model = NonRequired

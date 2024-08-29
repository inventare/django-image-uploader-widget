# Change Accept Formats

Like as the Widget `accept` attribute, see [reference here](../widget/04-accept.md), we have an way to customize the accept of the `ImageUploaderInline`. To customize it, use the `accept` property inside an class that inherits from `ImageUploaderInline`, like:

```python
from image_uploader_widget.admin import ImageUploaderInline
from . import models

class InlineEditor(ImageUploaderInline):
    model = models.InlineItem
    accept = "image/jpeg"
```

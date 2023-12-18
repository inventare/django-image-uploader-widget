---
sidebar_position: 1
---

# Colors

To customize the image uploader widget colors you can use your own css file to override the css variables defined by the `image-uploader-inline.css` and `image-uploader-widget.css`. See an example, taken from another personal private project:

```scss
body {
    --iuw-background: #{$dashdark} !important;
    --iuw-border-color: #{$dashborder} !important;
    --iuw-color: #{$dashgray} !important;
    --iuw-placeholder-text-color: #{$dashgray} !important;
    --iuw-dropzone-background: #{$dashlight} !important;
    --iuw-image-preview-border: #{$dashborder} !important;
    --iuw-image-preview-shadow: rgba(0, 0, 0, 0.3);
    --iuw-add-image-background: #{$dashlight} !important;
    --iuw-add-image-color: #{$dashgray} !important;
}
```

**Observation**: To see better the variables name, check the css file at the GitHub repository: [here](https://github.com/inventare/django-image-uploader-widget/blob/main/image_uploader_widget/static/admin/css/image-uploader-inline.css) or [here](https://github.com/inventare/django-image-uploader-widget/blob/main/image_uploader_widget/static/admin/css/image-uploader-widget.css).

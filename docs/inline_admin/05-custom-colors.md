# Custom Colors

To customize the image uploader inline colors you can use your own css file to override the css variables defined by the `image-uploader-inline.css`. See an example:

```scss
body {
    --iuw-background: #FFF;
    --iuw-border-color: #CCC;
    --iuw-color: #333;
    --iuw-placeholder-text-color: #AAA;
    --iuw-placeholder-destak-color: #417690;
    --iuw-dropzone-background: rgba(255, 255, 255, 0.8);
    --iuw-image-preview-border: #BFBFBF;
    --iuw-image-preview-shadow: rgba(0, 0, 0, 0.3);
    --iuw-add-image-background: #EFEFEF;
    --iuw-add-image-color: #AAA;
}
```

**Observation**: To see better the variables name, check the css file at the GitHub repository: [here](https://github.com/inventare/django-image-uploader-widget/blob/main/image_uploader_widget/static/image_uploader_widget/css/image-uploader-inline.css).

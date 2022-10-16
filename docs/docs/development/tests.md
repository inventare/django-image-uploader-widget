---
sidebar_position: 1
---

# Tests

To maintain the integrity of the features of this project we have written some integration tests to grant that main features of the widget and inline admin is really good.

:::note Why not unit tests?
In the decision to write the tests we opted for writing only integration tests using the selenium. And the reason for it is: our project uses much more JavaScript for web browser than Python code for back-end and runs in high coupling with the django-admin. In this context, unit tests are expendable.
:::

:::note Some unit tests
In the note block above i talked about not using unit test cases, and in the decisions of the issue [#77](https://github.com/inventare/django-image-uploader-widget/issues/77) we decided to add one unit test for the translation of the widget ([tests/widget_customized.py](https://github.com/inventare/django-image-uploader-widget/blob/main/image_uploader_widget_demo/tests/widget_customized.py#L5)).
:::

## Some Tests Decisions and Workarounds

When testing with selenium is not possible to hack the file picker to choose some file. And in this project, in some moments we use an *temporary file input* for choosing files without compromise the current choosed file. Based on those context, to test correctly fires to onClick event of the *temporary file input*, we added an JavaScript to add an onClick event showing an alert and test for this alert into the screen.

### An test project

For easy testing, we used the **demo** project `image_uploader_widget_demo` for writing base models for test add the tests for this project instead of the main component project.

## Test Cases

You can read (or contribute, if you want to improve this project) the test cases inside the `image_uploader_widget_demo` inside the github repository [here](https://github.com/inventare/django-image-uploader-widget/tree/main/image_uploader_widget_demo/tests).

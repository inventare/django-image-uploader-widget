from playwright.sync_api import Page

class _AssertInputFileClicked:
    def __init__(
        self,
        page: Page,
        input_selector=".form-row.field-image input[type=file]",
        index=0,
    ):
        self.page = page
        self.input_selector = input_selector
        self.index = index

    def __enter__(self):
        injected_javascript = (
            "async () => {"
            "   window.result = false;"
            f'  const inputs = document.querySelectorAll("{self.input_selector}");'
            f"  const input = inputs[{self.index}];"
            '   input.addEventListener("click", (e) => { e.preventDefault(); window.result = true; });'
            "};"
        )
        self.page.evaluate(injected_javascript)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        result = str(self.page.evaluate_handle("window.result"))
        assert result == "true"

def assert_input_file_clicked(
    page: Page,
    input_selector=".form-row.field-image input[type=file]",
    index=0
):
    return _AssertInputFileClicked(page, input_selector, index)

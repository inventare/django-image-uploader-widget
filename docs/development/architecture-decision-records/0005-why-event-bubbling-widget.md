# ADR 0005: Why using event bubbling on widget

| :date: {: .adr-emoji }         | August 2024. {: .adr-text}                                      |
| :----------------------------: | :-------------------------------------------------------------- |
| :writing_hand: {: .adr-emoji } | [Eduardo Oliveira](https://github.com/EduardoJM) {: .adr-text } |

## Context

We decided to add out of box support for HTMX on this package and we need to choice the way to do this.

## Decision Drivers

- We need to add out of box support for HTMX: the HTMX do a swap and, then, the widget is ready to use, without need of call anything in **JavaScript**.
- We need to change our scripts and code to support it.

## Considered Options

We considered only the two options bellow:

- Add initialization support on the [htmx:afterSwap](https://v1.htmx.org/events/#htmx:afterSwap) event.
- Rewrite the JavaScript to use **Event Bubbling**, and change the responsibility of adjusts the render to templates, to dispense the initialization of the widget.

## Decision

We decided to rewrite the JavaScript to use **Event Bubbling**, and change the responsibility of adjusts the render to templates, to dispense the initialization of the widget, for some reasons:

- This way we add support too for other libraries that works with ajax style requests and is not **HTMX**.
- Transfer the responsability of rendering from JavaScript to template engines make more easy to customize the widget.
- Remove dependêncies from **jQuery**.

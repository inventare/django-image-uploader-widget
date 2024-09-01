# ADR 0006: Why enforce light theme by class?

| :date: {: .adr-emoji }         | September 2024. {: .adr-text}                                      |
| :----------------------------: | :-------------------------------------------------------------- |
| :writing_hand: {: .adr-emoji } | [Eduardo Oliveira](https://github.com/EduardoJM) {: .adr-text } |

## Context

The theme toggle, for django-admin, was added in [django 4.2](https://docs.djangoproject.com/en/4.2/releases/4.2/#django-contrib-admin). On the versions before this, when the dark theme is available for the admin, the [prefers-color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme) is used to use dark theme. On this package, we used both `prefers-color-scheme` and theme toggle support for determine the colors.

## Decision Drivers

- We need a way to force light theme on the widget to use without django-admin in full light appearance.

## Decision

To force light theme, we decided to add a class `.iuw-light` that force the theme variables to light and a `.iuw-dark` to force the theme variables to dark.

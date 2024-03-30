# ADR 0002: Why UI regression tests?

| :date: {: .adr-emoji }         | November 2023. {: .adr-text}                                    |
| :----------------------------: | :-------------------------------------------------------------- |
| :writing_hand: {: .adr-emoji } | [Eduardo Oliveira](https://github.com/EduardoJM) {: .adr-text } |

## Context

Some Django versions have significant visual differences. One example of this was documented on the issue [#96](https://github.com/inventare/django-image-uploader-widget/issues/96#issuecomment-1690740705).

## Decision Drivers

- We need to maintain retrocompatibility with various versions of Django.
- We need to grant the behaviour and the visual of the widget and inline in various versions of Django.

## Decision

To grant the visual of the widget and the inlines in various versions of Django, we decided to implements UI regression tests using the selenium (currently **playwright**) to take screenshots of the root element of the widget or inline and compare it with other saved screenshots.

Some problems and solutions that are writed for this project was found at my [blogpost](https://dev.to/eduardojm/lidando-com-regressao-visual-enfrentando-desafios-com-django-selenium-e-pillow-o8d) in brazillian portuguese.

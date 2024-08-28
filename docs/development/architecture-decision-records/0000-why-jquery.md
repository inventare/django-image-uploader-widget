# ADR 0000: Why jQuery?

| :date: {: .adr-emoji }         | November 2023. {: .adr-text}                                    |
| :----------------------------: | :-------------------------------------------------------------- |
| :writing_hand: {: .adr-emoji } | [Eduardo Oliveira](https://github.com/EduardoJM) {: .adr-text } |

## Context

Some of the `django-admin` scripts uses jQuery and we need to decide if we will use jQuery or not.

## Decision Drivers

- We need to maintain retrocompatibility with `Django 3.2` and new versions of `Django 4.x`.
- Our code don't have any dependencies to jQuery.

## Decision

At the `Django 3.2` and `Django 4.0` version, the `inlines.js` script (a script to control the inlines form inside the `django-admin`) dispatch `formset:added` event as jQuery `trigger()` event. This event can't be catched using native event handlers [[inlines.js#L91](https://github.com/django/django/blob/stable/3.2.x/django/contrib/admin/static/admin/js/inlines.js#L91)].

At `Django 4.1.x` version, this event dispatch was transformed to use native browser `CustomEvent` [[inlines.js#L91](https://github.com/django/django/blob/stable/4.1.x/django/contrib/admin/static/admin/js/inlines.js#L91)]. The other side way is valid: if we dispatched the event using native `CustomEvent` can be catched by the jQuery `on()` method. Then, to maintain compatibility with `Django 4.0.x` and `Django 3.2.x`, we decided to use jQuery at this project with one restriction:

- jQuery is used, and your use is alowed only in this case, to start the widget inside inlines formset.

!!! info "Version Information"

    jQuery is no more used on 0.6.0+ versions because the widget no need more initialization. This is commented on [ADR 0005: Why using event bubbling on widget](./0005-why-event-bubbling-widget.md)


# Force dark or light color scheme

On the [ADR 0006](../development/architecture-decision-records/0006-why-enforce-light-theme-by-class.md) we discuted a way to force color scheme (`dark` or `light`) to ensure widget color scheme outside of `django-admin`. The two cases bellow is tested using [UI regression](../development/architecture-decision-records/0002-why-ui-regression-tests.md) tests. This is the same way that we implemented on default widget and this is [documented here](../widget/07-force-color-scheme.md).


## Light theme

To enforce light widget, use `.iuw-light` class:

```html
<div class="iuw-light">
  {{ form }}
</div>
```

## Dark theme

To enforce dark widget, use `.iuw-dark` class:

```html
<div class="iuw-dark">
  {{ form }}
</div>
```

# ADR 0004: Why Mkdocs instead of docusaurus?

| :date: {: .adr-emoji }         | March 2024. {: .adr-text}                                    |
| :----------------------------: | :-------------------------------------------------------------- |
| :writing_hand: {: .adr-emoji } | [Eduardo Oliveira](https://github.com/EduardoJM) {: .adr-text } |

## Context

The documentation of the `django-image-uploader-widget` is full based on a [docusaurus](https://docusaurus.io/) documentation generation. This was decided, by me, for some reasons. The most important reason is: i have a large expertise working with JavaScript and i known the docusaurus usage and, then, i created the documentation with small effort.

Based on the first paragraph, we need to talk about one point: the docusaurus insert much complexity for the documentation with some `React` code and various node configurations, only for the documentation.

## Decision Drivers

- We need to simplify the tolling for this open-source package.
- Docusaurus insert much complexity and configuration files.
- Docusaurus is not known by most part of the python and django community.

## Considered Options

We considered the two options bellow:

- Maintain the `docusaurus` documentation and continue using it.
- Change to the `mkdocs` documentation.

## Decision

We decided to change the documentation to the `mkdocs` based on some points:

- Move all the possible tolling to the python community tools.
- The `FastAPI` documentation, writen in `mkdocs` is a very important success case for `mkdocs`.
- We have some tooling, like [mkautodoc](https://github.com/tomchristie/mkautodoc) to better support things like the `API Reference` full integrated from code to documentation.

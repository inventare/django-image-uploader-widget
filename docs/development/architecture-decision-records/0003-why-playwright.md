# ADR 0003: Why Playwright?

| :date: {: .adr-emoji }         | December 2023. {: .adr-text}                                    |
| :----------------------------: | :-------------------------------------------------------------- |
| :writing_hand: {: .adr-emoji } | [Eduardo Oliveira](https://github.com/EduardoJM) {: .adr-text } |

## Context

The selenium is very slow to run our tests and we decided to switch from the selenium to another e2e testing framework.

## Decision Drivers

- We need to switch to another e2e testing framework to test our widget. See the [ADR 0001](./0001-why-functional-tests.md) and the [ADR 0002](./0002-why-ui-regression-tests.md) to understand the motivation for the e2e testing framework.
- We need to get a testing framework that we can rewrite the tests fast.
- we need to get support to take screenshot of elements for the [ADR 0002](./0002-why-ui-regression-tests.md).

## Considered Options

We considered only the two options bellow:

- **Playwright:** enables reliable end-to-end testing for modern web apps.
- **Selenium:** automates browsers.

## Decision

The playwright API is a little bit more semantic than the selenium and is faster. For this reason, we decided to use playwright and rewrite our integration and ui-regression tests with playwright.

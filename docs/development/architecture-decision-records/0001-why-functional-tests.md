# ADR 0001: Why functional tests?

| :date: {: .adr-emoji }         | November 2023. {: .adr-text}                                    |
| :----------------------------: | :-------------------------------------------------------------- |
| :writing_hand: {: .adr-emoji } | [Eduardo Oliveira](https://github.com/EduardoJM) {: .adr-text } |

## Context

To write tests to maintain the confiability of the project, we decided to write some tests. 

## Decision Drivers

- We need to write comprehensive tests.
- We need robust and well-tested tools.
- The less complexity the tests add to the codebase, better.

## Considered Options

- Write unit tests for django project and unit/integration tests for javascript using two separate tools (one for each stack).
- Write functional tests for django using selenium (currently **playwright**).

## Decision

To write tests with less possible complexity, we decided to write functional tests with selenium (currently **playwright**). The `django.contrib.staticfiles.testing.StaticLiveServerTestCase` is a goog approach to run the application with selenium or any other in-browser testing tool (currently **playwright**). We considered the possibility of use two separated test-cases, one for `django` and one for `javascript`, will increase the complexity. Based on this, the majority of our tests are functional (or e2e?) tests.

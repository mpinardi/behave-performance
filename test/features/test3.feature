@t3
Feature: My test 3

Scenario: scenario t3
    When Check 3
    When System out "Test 3"
    Then Wait for 50

Scenario Outline: scenario t3 2
    When System out "<value>"

Examples:
|value|
|best3|
|fun3|
|win3|
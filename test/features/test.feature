Feature: test

@only
@only1
Scenario: scenario 1
    When Check 2
    When System out "value out"
    Then Wait for 1000

@only2
Scenario Outline: scenario 2
    When System out "<value>"
    Then Verify successful

    Examples:
    |value|
    |test|
    |fun|
    |win|

@only3
Scenario: scenario 4 table error and undefinded
    Given I have the following veggies and meat:
    |Veggies|Meat   |
    |Beans  |Bacon  |
    |Onion  |Beef   |
    When Make a meal
    Then Check it tastes good
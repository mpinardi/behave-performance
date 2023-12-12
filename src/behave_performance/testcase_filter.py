from behave.tag_expression import make_tag_expression
from behave.model import Feature,Scenario

TAG_PATTERN = r'@(.*)(?=[ ,])|@.*(?=[@])|@.*'

class TestCaseFilter:
    """Filters testcases(behave models of Features,Scenarios) by passed in group text.
    """
    def __init__(self, test_cases:[Feature|Scenario]) -> None:
        self.test_cases = test_cases

    def filter(self, text:str) -> list:
        """Get behave models that match group text.

        Args:
            text (str): Group text.

        Returns:
            list: A list of all the matching test cases
        """
        filteredtest_cases = []
        for test_case in self.test_cases:
            if self.is_match(test_case, text):
                filteredtest_cases.append(test_case)
        return filteredtest_cases

    def is_match(self, test_case:[Feature|Scenario], text:str)->bool|None:
        """Checks if a test_case matches the passed in group text.

        Args:
            test_case (Feature | Scenario]): The test case to check.
            text (str): The group text to use for comparision.

        Returns: True if the test_case is a match else false.
            
        """
        if text.startswith('@'):
            tge = make_tag_expression(text)
            return test_case.should_run_with_tags(tge)
        elif test_case.location.filename.endswith(text) or test_case.location.filename.endswith(text + '.feature'):
            return True
        elif test_case.name == text:
            return True

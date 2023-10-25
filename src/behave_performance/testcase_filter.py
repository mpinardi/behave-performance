import re
from behave.tag_expression import make_tag_expression

TAG_PATTERN = r'@(.*)(?=[ ,])|@.*(?=[@])|@.*'

class TestCaseFilter:
    def __init__(self, test_cases):
        self.test_cases = test_cases

    def filter(self, text):
        filteredtest_cases = []
        for test_case in self.test_cases:
            if self.isMatch(test_case, text):
                filteredtest_cases.append(test_case)
        return filteredtest_cases

    def isMatch(self, test_case, text):
        if text.startswith('@'):
            tge = make_tag_expression(text)
            return test_case.should_run_with_tags(tge)
            # matches = re.findall(TAG_PATTERN, text)
            # for tag in test_case.tags:
            #     for m in matches:
            #         if tag == m:
            #             return True
        elif test_case.location.filename.endswith(text) or test_case.location.filename.endswith(text + '.feature'):
            return True

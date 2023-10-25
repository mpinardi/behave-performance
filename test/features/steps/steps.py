import sys
import time
from behave import given, when, then, step

@then('Wait for {num}')
@when('Wait for {num}')
def wait(context, num):
    time.sleep(int(num)/1000)

@when(u'Check {num}')
def check(context,num):
    pass

@when(u'System out "{value}"')
def sys_out(context,value):
    print(value)
    
@given(u'I have the following veggies and meat')
def has_veg(context):
    t = context.table

@when(u'Make a meal')
def make_meal(context):
    make = meal

@then(u'Verify successful')
def is_suc(context):
    assert(False)


import pytest
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
ex03_dir = os.path.join(src_dir, 'ex03')
sys.path.insert(0, ex03_dir)

from financial import get_financial_data

def test_returns_tuple():
    result = get_financial_data(ticker='MSFT', field='Total Revenue')
    assert isinstance(result, tuple), f"Expected tuple, got {type(result)}"
    assert len(result) > 0, "Empty tuple"
    assert isinstance(result[0], str), f"First element is not str, but {type(result[0])}. Test NOT passed"
    print("Test passed")

def test_correct_field_value():
    field = 'Total Revenue'
    result = get_financial_data(ticker='MSFT', field=field)
    assert result[0] == field, f"Expected {field}, got {result[0]}. Test NOT passed"

def test_invalid_ticker_exception():
    invalid_ticker = 'INVALID1234'

    with pytest.raises(Exception) as e_info:
        get_financial_data(ticker=invalid_ticker, field='Total Revenue')

    assert e_info.value is not None, "No exception for invalid ticker. Test NOT passed"

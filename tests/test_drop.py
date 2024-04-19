from rolldice import roll_dice
from hypothesis import given, note
from hypothesis import strategies as st


# This is a basic sanity check that avoids the need to parse the explanation string.
# If you roll N dice, and drop N-1, then the result has to be in the range of the die size.
@given(
    roll_count=st.integers(min_value=2, max_value=20),
    die_size=st.integers(min_value=2, max_value=100),
    op=st.sampled_from("Xx"),
)
def test_result_in_bounds(roll_count, die_size, op):
    drop_count = roll_count - 1
    expr = f"{roll_count}d{die_size}{op}{drop_count}"
    result, explanation = roll_dice(expr)
    note(f'expr={expr}, explanation={explanation}')
    assert 1 <= result <= die_size

@given(
    roll_count=st.integers(min_value=2, max_value=20),
    die_size=st.integers(min_value=2, max_value=100),
    op=st.sampled_from("Xx"),
    data=st.data()
)
def test_sum(roll_count, die_size, op, data):
    drop_count = data.draw(st.integers(min_value=1, max_value=roll_count - 1))
    expr = f"{roll_count}d{die_size}{op}{drop_count}"
    result, explanation = roll_dice(expr)
    included, dropped = explanation.strip('[]').split(' ~~ ')
    included_rolls = [int(x) for x in included.split(',')]
    dropped_rolls = [int(x) for x in dropped.split(',')]
    assert(len(dropped_rolls) == drop_count)
    assert(len(included_rolls) + len(dropped_rolls) == roll_count)
    included_sum = sum(included_rolls)
    assert(result == included_sum)

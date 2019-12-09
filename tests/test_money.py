from money.money import Expression, Bank, Sum, Money


def test_equality():
    assert Money.dollar(5) == Money.dollar(5)
    assert Money.dollar(5) != Money.dollar(6)

    assert Money.dollar(5) != Money.franc(5)


def test_multiplication():
    five: Money = Money.dollar(5)
    assert Money.dollar(10) == five * 2
    assert Money.dollar(15) == five * 3


def test_currency():
    assert Money.dollar(1).currency == "USD"
    assert Money.franc(1).currency == "CHF"


def test_simple_addition():
    five: Money = Money.dollar(5)
    # "sum" is a reserved keyword in Python, so everything that is named "sum"
    # in the books example will be named "sum_" for consistencies sake
    sum_ = five + five
    bank = Bank()
    reduced = bank.reduce(sum_, "USD")
    assert reduced == Money.dollar(10)


def test_plus_returns_sum():
    five = Money.dollar(5)
    result = five + five
    assert five == result.augend
    assert five == result.addend


def test_reduce_sum():
    sum_ = Sum(Money.dollar(3), Money.dollar(4))
    bank = Bank()
    result = bank.reduce(sum_, "USD")
    assert result == Money.dollar(7)


def test_reduce_money():
    bank = Bank()
    result = bank.reduce(Money.dollar(1), "USD")
    assert result == Money.dollar(1)


def test_reduce_money_different_currency():
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)
    result = bank.reduce(Money.franc(2), "USD")
    assert result == Money.dollar(1)


def test_identity_rate():
    assert Bank().rate("USD", "USD") == 1


def test_mixed_addition():
    five_dollars = Money.dollar(5)
    ten_francs = Money.franc(10)
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)
    result = bank.reduce(five_dollars + ten_francs, "USD")
    assert result == Money.dollar(10)


def test_sum_plus_money():
    five_dollars = Money.dollar(5)
    ten_francs = Money.franc(10)
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)
    sum_ = Sum(five_dollars, ten_francs) + five_dollars
    result = bank.reduce(sum_, "USD")
    assert result == Money.dollar(15)


def test_sum_times():
    five_dollars = Money.dollar(5)
    ten_francs = Money.franc(10)
    bank = Bank()
    bank.add_rate("CHF", "USD", 2)
    sum_ = Sum(five_dollars, ten_francs) * 2
    result = bank.reduce(sum_, "USD")
    assert result == Money.dollar(20)

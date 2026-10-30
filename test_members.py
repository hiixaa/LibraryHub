import pytest

from members import StudentMember, RegularMember, PremiumMember


def test_student_member():
    student = StudentMember("M001", "Asha Raman", "asha@example.com")

    assert student.max_items == 3
    assert student.loan_period() == 14
    assert student.daily_fine_rate == 2


def test_regular_member():
    regular = RegularMember("M002", "Rahul Mehta", "rahul@example.com")

    assert regular.max_items == 5
    assert regular.loan_period() == 21
    assert regular.daily_fine_rate == 5


def test_premium_member():
    premium = PremiumMember("M003", "Sneha Iyer", "sneha@example.com")

    assert premium.max_items == 10
    assert premium.loan_period() == 30
    assert premium.daily_fine_rate == 3


def test_invalid_member_email():
    student = StudentMember("M001", "Asha Raman", "asha@example.com")

    with pytest.raises(ValueError):
        student.email = "invalid-email"

@pytest.mark.parametrize(
    "member_class, member_id, name, email, max_items, loan_days, fine_rate",
    [
        (StudentMember, "M001", "Asha", "asha@example.com", 3, 14, 2),
        (RegularMember, "M002", "Rahul", "rahul@example.com", 5, 21, 5),
        (PremiumMember, "M003", "Sneha", "sneha@example.com", 10, 30, 3),
    ]
)
def test_member_types_parameterized(
    member_class, member_id, name, email,
    max_items, loan_days, fine_rate
):
    member = member_class(member_id, name, email)

    assert member.max_items == max_items
    assert member.loan_period() == loan_days
    assert member.daily_fine_rate == fine_rate
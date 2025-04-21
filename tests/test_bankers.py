# manual_test.py
from core.banker import BankersAlgorithm

# Test 1: Safe state
def test_safe_state():
    banker = BankersAlgorithm(
        available=[10, 5, 7],  # Increased resources
        max_need=[
            [7, 5, 3],  # Process 0
            [3, 2, 2]   # Process 1
        ],
        allocated=[
            [0, 1, 0],  # Process 0
            [2, 0, 0]    # Process 1
        ]
    )
    is_safe, seq = banker.is_safe()
    print(f"Test 1 - Safe State: {is_safe}, Sequence: {seq}")
    assert is_safe == True
    assert len(seq) == 2  # Ensure all processes are in the sequence

# Test 2: Unsafe request
def test_unsafe_request():
    banker = BankersAlgorithm(
        available=[2, 1, 0],
        max_need=[
            [3, 3, 2],
            [1, 2, 3]
        ],
        allocated=[
            [1, 2, 0],
            [1, 0, 1]
        ]
    )
    is_safe, seq = banker.is_safe()
    print(f"Test 2 - Safe State: {is_safe}, Sequence: {seq}")
    result = banker.request_resources(0, [3, 1, 0])  # Should fail
    print(f"Unsafe Request: result = {result}")
    assert result == False

if __name__ == "__main__":
    test_safe_state()
    test_unsafe_request()
    print("All manual tests passed!")
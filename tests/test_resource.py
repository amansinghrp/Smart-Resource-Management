from core.resource import Resource

def test_resource_allocation():
    r = Resource(rid=0, total=5)
    assert r.available == 5
    
    # Test successful allocation
    assert r.allocate(3) == True
    assert r.available == 2
    
    # Test overallocation
    assert r.allocate(3) == False  # Only 2 available
    
    # Test release
    r.release(2)
    assert r.available == 4
    print("✓ Resource tests passed!")
    print(r)

if __name__ == "__main__":
    test_resource_allocation()
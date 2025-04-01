from core.process import Process

def test_process_creation():
    p = Process(pid=1, max_resources=[3, 1, 2])
    assert p.pid == 1
    assert p.max == [3, 1, 2]
    assert p.allocation == [0, 0, 0]
    assert p.need == [3, 1, 2]
    print("Process created successfully: ", p)

if __name__ == '__main__':
    test_process_creation()
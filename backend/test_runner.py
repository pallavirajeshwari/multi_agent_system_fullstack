import os
import json
from main import run_goal

def evaluate(file_path):
    with open(file_path) as f:
        test_case = json.load(f)
    
    goal = test_case["goal"]
    expected = test_case["expected_output"].lower()
    actual = run_goal(goal).lower()

    print(f"\n🧪 Testing Goal: {goal}")
    print(f"Expected: {expected}")
    print(f"Actual:   {actual}")

    if expected in actual:
        print("✅ Test Passed")
        return True
    else:
        print("❌ Test Failed")
        return False

def run_all():
    test_dir = "evaluations"
    total, passed = 0, 0

    for filename in os.listdir(test_dir):
        if filename.endswith(".json"):
            path = os.path.join(test_dir, filename)
            if evaluate(path):
                passed += 1
            total += 1

    print(f"\n🎯 Test Summary: {passed}/{total} Passed")

if __name__ == "__main__":
    run_all()

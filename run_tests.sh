#!/bin/bash
# Test runner for SmartSupport AI

echo "=================================="
echo "SmartSupport AI - Test Suite"
echo "=================================="
echo ""

# Run unit tests
echo "Running unit tests..."
python -m unittest discover -s backend/tests -p 'test_*.py' -v

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
    exit 0
else
    echo ""
    echo "❌ Some tests failed!"
    exit 1
fi


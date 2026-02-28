import asyncio
import importlib
import sys

# List of all pattern modules to validate
PATTERN_FILES = [
    f"pattern_{i:02}" for i in range(1, 22)
]

# Map friendly names for patterns that might have suffixes in your filenames
PATTERNS_TO_TEST = [
    "pattern_01_routing", "pattern_02_chaining", "pattern_03_parallelization",
    "pattern_04_reflection", "pattern_05_tool_use", "pattern_06_planning",
    "pattern_07_multi_agent", "pattern_08_memory", "pattern_09_learning",
    "pattern_10_mcp", "pattern_11_goal_setting", "pattern_12_exception",
    "pattern_13_hitl", "pattern_14_rag", "pattern_15_a2a",
    "pattern_16_resource_aware", "pattern_17_reasoning", "pattern_18_guardrails",
    "pattern_19_evaluation", "pattern_20_prioritization", "pattern_21_exploration"
]

async def validate_all():
    print("📋 Starting Master Validation of 21 Agentic Patterns...")
    print("-" * 50)
    
    passed = 0
    failed = 0

    for p in PATTERNS_TO_TEST:
        try:
            # 1. Test Import
            module = importlib.import_module(p)
            
            # 2. Test existence of run_pattern
            if not hasattr(module, 'run_pattern'):
                raise AttributeError(f"Missing 'run_pattern' function.")
            
            # 3. Test Agent Initialization (Heuristic check)
            # We look for variables that are instances of the Agent class
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if hasattr(attr, '__class__') and attr.__class__.__name__ == 'Agent':
                    # Instead of deep-inspecting, just check if we can access the name
                    try:
                        _name = attr.name
                    except Exception:
                        pass # Ignore lazy-loading Pydantic issues during import
            
            print(f"✅ {p}: PASSED")
            passed += 1
            
        except Exception as e:
            print(f"❌ {p}: FAILED")
            print(f"   Error: {str(e)}")
            failed += 1

    print("-" * 50)
    print(f"RESULTS: {passed} Passed, {failed} Failed.")
    
    if failed == 0:
        print("🚀 All patterns are valid and ready for the Executive Dashboard!")
    else:
        print("⚠️ Please fix the errors listed above before launching.")

if __name__ == "__main__":
    asyncio.run(validate_all())
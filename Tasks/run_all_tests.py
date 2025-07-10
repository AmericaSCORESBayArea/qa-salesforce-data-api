#!/usr/bin/env python3
"""
Main Test Runner for API Test Suite

This script discovers and runs all test files in the project.
It provides a unified entry point for running all API tests.

Usage:
    python run_all_tests.py
    python run_all_tests.py --verbose
    python run_all_tests.py --help
"""

import os
import sys
import unittest
import argparse
from pathlib import Path
from typing import List, Optional


class TestRunner:
    """Main test runner that discovers and executes all test files."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.test_modules = []
        self.results = []
        
    def discover_tests(self, start_dir: str = '.', pattern: str = '*test*.py') -> List[str]:
        """
        Discover all test files in the project.
        
        Args:
            start_dir: Directory to start searching from
            pattern: File pattern to match (default: '*test*.py')
            
        Returns:
            List of discovered test file paths
        """
        test_files = []
        project_root = Path(start_dir).resolve()
        
        # Find all Python files matching the pattern
        for file_path in project_root.rglob(pattern):
            if file_path.is_file() and file_path.suffix == '.py':
                # Skip __pycache__ and other non-test directories
                if '__pycache__' not in str(file_path):
                    test_files.append(str(file_path))
                    
        # Also look for files starting with 'QA_' (like QA_Get_Task_WithContact.py)
        for file_path in project_root.rglob('QA_*.py'):
            if file_path.is_file() and str(file_path) not in test_files:
                if '__pycache__' not in str(file_path):
                    test_files.append(str(file_path))
        
        return sorted(test_files)
    
    def run_test_file(self, test_file_path: str) -> bool:
        """
        Run a single test file and return success status.
        
        Args:
            test_file_path: Path to the test file
            
        Returns:
            True if all tests passed, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"RUNNING: {test_file_path}")
        print(f"{'='*60}")
        
        try:
            # Add the test file's directory to Python path
            test_dir = os.path.dirname(os.path.abspath(test_file_path))
            if test_dir not in sys.path:
                sys.path.insert(0, test_dir)
            
            # Import the test module
            module_name = os.path.splitext(os.path.basename(test_file_path))[0]
            spec = unittest.util.spec_from_file_location(module_name, test_file_path)
            if spec is None:
                print(f"ERROR: Could not load spec for {test_file_path}")
                return False
                
            module = unittest.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Create test suite from the module
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(module)
            
            # Run the tests
            runner = unittest.TextTestRunner(
                verbosity=2 if self.verbose else 1,
                buffer=False,
                stream=sys.stdout
            )
            result = runner.run(suite)
            
            # Store results
            self.results.append({
                'file': test_file_path,
                'tests_run': result.testsRun,
                'failures': len(result.failures),
                'errors': len(result.errors),
                'success': result.wasSuccessful()
            })
            
            return result.wasSuccessful()
            
        except Exception as e:
            print(f"ERROR running {test_file_path}: {e}")
            self.results.append({
                'file': test_file_path,
                'tests_run': 0,
                'failures': 0,
                'errors': 1,
                'success': False
            })
            return False
    
    def run_all_tests(self) -> bool:
        """
        Discover and run all tests in the project.
        
        Returns:
            True if all tests passed, False otherwise
        """
        print("🔍 Discovering test files...")
        test_files = self.discover_tests()
        
        if not test_files:
            print("❌ No test files found!")
            return False
        
        print(f"📁 Found {len(test_files)} test file(s):")
        for test_file in test_files:
            print(f"  - {test_file}")
        
        print(f"\n🚀 Running all tests...")
        
        all_passed = True
        for test_file in test_files:
            success = self.run_test_file(test_file)
            if not success:
                all_passed = False
        
        self.print_summary()
        return all_passed
    
    def print_summary(self):
        """Print a summary of all test results."""
        print(f"\n{'='*60}")
        print("📊 TEST SUMMARY")
        print(f"{'='*60}")
        
        total_tests = sum(r['tests_run'] for r in self.results)
        total_failures = sum(r['failures'] for r in self.results)
        total_errors = sum(r['errors'] for r in self.results)
        files_passed = sum(1 for r in self.results if r['success'])
        
        print(f"Files run: {len(self.results)}")
        print(f"Files passed: {files_passed}")
        print(f"Files failed: {len(self.results) - files_passed}")
        print(f"Total tests: {total_tests}")
        print(f"Total failures: {total_failures}")
        print(f"Total errors: {total_errors}")
        
        if total_failures == 0 and total_errors == 0:
            print("\n✅ ALL TESTS PASSED!")
        else:
            print(f"\n❌ {total_failures + total_errors} TEST(S) FAILED")
            
        print(f"\nDetailed results:")
        for result in self.results:
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"  {status} {result['file']} "
                  f"({result['tests_run']} tests, "
                  f"{result['failures']} failures, "
                  f"{result['errors']} errors)")


def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(
        description="Run all API tests in the project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_all_tests.py              # Run all tests
  python run_all_tests.py --verbose    # Run with verbose output
  python run_all_tests.py -v           # Same as --verbose
        """
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Create and run the test runner
    runner = TestRunner(verbose=args.verbose)
    success = runner.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
import unittest
from package_sorter import sort


class TestPackageSorter(unittest.TestCase):
    """Test cases for the package sorting function"""
    
    def test_standard_packages(self):
        """Test packages that should be classified as STANDARD"""
        # Small package, light weight
        self.assertEqual(sort(10, 10, 10, 5), "STANDARD")
        
        # Medium package, still under all thresholds
        self.assertEqual(sort(99, 99, 99, 19), "STANDARD")
        
        # Just under volume threshold
        self.assertEqual(sort(99, 99, 101, 10), "STANDARD")
    
    def test_bulky_by_volume(self):
        """Test packages that are bulky due to volume >= 1,000,000 cm³"""
        # Exactly at volume threshold, not heavy
        self.assertEqual(sort(100, 100, 100, 10), "SPECIAL")
        
        # Over volume threshold, not heavy
        self.assertEqual(sort(150, 100, 100, 15), "SPECIAL")
        
        # Large volume, just under heavy threshold
        self.assertEqual(sort(200, 100, 100, 19.9), "SPECIAL")
    
    def test_bulky_by_dimension(self):
        """Test packages that are bulky due to one dimension >= 150 cm"""
        # Width exactly 150
        self.assertEqual(sort(150, 10, 10, 10), "SPECIAL")
        
        # Height exactly 150
        self.assertEqual(sort(10, 150, 10, 10), "SPECIAL")
        
        # Length exactly 150
        self.assertEqual(sort(10, 10, 150, 10), "SPECIAL")
        
        # One dimension over 150, small volume
        self.assertEqual(sort(200, 5, 5, 15), "SPECIAL")
    
    def test_heavy_packages(self):
        """Test packages that are heavy (mass >= 20 kg)"""
        # Exactly at heavy threshold
        self.assertEqual(sort(50, 50, 50, 20), "SPECIAL")
        
        # Over heavy threshold, small dimensions
        self.assertEqual(sort(10, 10, 10, 25), "SPECIAL")
        
        # Very heavy, but not bulky
        self.assertEqual(sort(100, 100, 50, 100), "SPECIAL")
    
    def test_rejected_packages(self):
        """Test packages that are both bulky and heavy"""
        # Both bulky (volume) and heavy
        self.assertEqual(sort(100, 100, 100, 20), "REJECTED")
        
        # Both bulky (dimension) and heavy
        self.assertEqual(sort(150, 50, 50, 25), "REJECTED")
        
        # Extremely large and heavy
        self.assertEqual(sort(200, 200, 200, 50), "REJECTED")
        
        # Bulky by dimension and volume, also heavy
        self.assertEqual(sort(160, 120, 80, 30), "REJECTED")
    
    def test_boundary_conditions(self):
        """Test exact boundary values"""
        # Volume exactly 1,000,000, mass exactly 20
        self.assertEqual(sort(100, 100, 100, 20), "REJECTED")
        
        # Volume just under 1,000,000, mass just under 20
        self.assertEqual(sort(99.9, 100, 100, 19.9), "STANDARD")
        
        # Dimension exactly 150, mass just under 20
        self.assertEqual(sort(150, 50, 50, 19.9), "SPECIAL")
        
        # Dimension just under 150, mass exactly 20
        self.assertEqual(sort(149.9, 50, 50, 20), "SPECIAL")
    
    def test_edge_cases(self):
        """Test edge cases with extreme values"""
        # Very small package
        self.assertEqual(sort(1, 1, 1, 0.1), "STANDARD")
        
        # Very large but thin package (like a poster tube)
        self.assertEqual(sort(200, 5, 5, 5), "SPECIAL")
        
        # Compact but extremely heavy (like lead)
        self.assertEqual(sort(10, 10, 10, 100), "SPECIAL")
        
        # Decimal dimensions and mass
        self.assertEqual(sort(99.5, 99.5, 99.5, 19.5), "STANDARD")
    
    def test_invalid_inputs(self):
        """Test that invalid inputs raise appropriate errors"""
        # Zero dimensions
        with self.assertRaises(ValueError):
            sort(0, 100, 100, 10)
        
        # Negative dimensions
        with self.assertRaises(ValueError):
            sort(-10, 100, 100, 10)
        
        # Zero mass
        with self.assertRaises(ValueError):
            sort(100, 100, 100, 0)
        
        # Negative mass
        with self.assertRaises(ValueError):
            sort(100, 100, 100, -5)


class TestRealWorldScenarios(unittest.TestCase):
    """Test real-world package scenarios"""
    
    def test_common_packages(self):
        """Test typical e-commerce packages"""
        # Small electronics box
        self.assertEqual(sort(30, 20, 10, 2), "STANDARD")
        
        # Medium shipping box
        self.assertEqual(sort(60, 40, 40, 5), "STANDARD")
        
        # Large appliance box
        self.assertEqual(sort(120, 80, 80, 25), "SPECIAL")
        
        # Furniture (large and heavy)
        self.assertEqual(sort(180, 90, 60, 35), "REJECTED")
    
    def test_special_shapes(self):
        """Test unusually shaped packages"""
        # Long thin package (like a golf club)
        self.assertEqual(sort(200, 10, 10, 3), "SPECIAL")
        
        # Flat large package (like a painting)
        self.assertEqual(sort(140, 100, 5, 8), "STANDARD")
        
        # Tall package (like a standing mirror)
        self.assertEqual(sort(80, 160, 15, 18), "SPECIAL")


def run_tests():
    """Run all tests and display results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestPackageSorter))
    suite.addTests(loader.loadTestsFromTestCase(TestRealWorldScenarios))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)

"""
Main entry point for My LLM Digital Twin project.
"""
import numpy as np
import pandas as pd
import requests
import openai
from settings import settings

def test_dependencies():
    """Test that all major dependencies are working."""
    print("� Testing Dependencies:")
    print(f"  ✅ NumPy: {np.__version__}")
    print(f"  ✅ Pandas: {pd.__version__}")
    print(f"  ✅ Requests: {requests.__version__}")
    print(f"  ✅ OpenAI: {openai.__version__}")
    
    # Test numpy functionality
    test_array = np.array([1, 2, 3, 4, 5])
    print(f"  ✅ NumPy test - Array mean: {np.mean(test_array)}")
    
    # Test pandas functionality
    df = pd.DataFrame({'test': [1, 2, 3]})
    print(f"  ✅ Pandas test - DataFrame shape: {df.shape}")

def main():
    """Main function to start the application."""
    print(f"� Starting {settings.PROJECT_NAME}")
    print(f"Debug mode: {settings.DEBUG}")
    print(f"Configuration complete: {settings.is_configured}")
    
    test_dependencies()
    
    if settings.DEBUG:
        print("\n� Running in development mode...")
        try:
            response = requests.get("https://httpbin.org/json", timeout=5)
            print(f"  ✅ HTTP test - Status: {response.status_code}")
        except requests.RequestException as e:
            print(f"  ⚠️  HTTP test failed (this is okay): {e}")
    
    print("\n� Ready to build LLM features!")

if __name__ == "__main__":
    main()

import sys
from src.metrics.complexity import ComplexityAnalyser

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <file.py>")
        return
    
    analyser = ComplexityAnalyser()
    with open(sys.argv[1], 'r') as f:
        res = analyser.analyse_source(f.read(), sys.argv[1])
    
    print(f"File: {res.filepath}")
    print(f"Average Complexity: {res.average_complexity}")

if __name__ == "__main__":
    main()
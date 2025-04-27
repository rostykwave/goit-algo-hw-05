import timeit
import numpy as np

def build_shift_table(pattern):
    """
    Build the shift table for the Boyer-Moore algorithm.
    """
    table = {}
    pattern_length = len(pattern)
    
    # Fill the table with the max shift
    for i in range(pattern_length - 1):
        table[pattern[i]] = pattern_length - i - 1
    
    # If the character is not in the pattern, it will be shifted by the length of the pattern
    table.setdefault(pattern[-1], pattern_length)
    
    return table

def boyer_moore_search(text, pattern):
    """
    Implementation of the Boyer-Moore string searching algorithm.
    """
    pattern_length = len(pattern)
    text_length = len(text)
    
    if pattern_length > text_length:
        return -1
    
    if not pattern:
        return 0
    
    # Build the shift table
    shift_table = build_shift_table(pattern)
    
    # Start from the end of the pattern
    i = pattern_length - 1
    
    while i < text_length:
        j = pattern_length - 1
        k = i
        
        # Compare characters from right to left
        while j >= 0 and text[k] == pattern[j]:
            j -= 1
            k -= 1
        
        if j == -1:  # Pattern found
            return k + 1
        
        # Shift the pattern
        if text[k] in shift_table:
            i += shift_table[text[k]]
        else:
            i += pattern_length
    
    return -1  # Pattern not found

def compute_lps(pattern):
    """
    Compute the Longest Proper Prefix which is also Suffix array for KMP algorithm.
    """
    lps = [0] * len(pattern)
    length = 0
    i = 1
    
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    return lps

def kmp_search(text, pattern):
    """
    Implementation of the Knuth-Morris-Pratt string searching algorithm.
    """
    if not pattern:
        return 0
        
    n = len(text)
    m = len(pattern)
    
    if m > n:
        return -1
    
    # Compute the LPS array
    lps = compute_lps(pattern)
    
    i = 0  # Index for text
    j = 0  # Index for pattern
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == m:  # Pattern found
            return i - j
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return -1  # Pattern not found

def rabin_karp_search(text, pattern):
    """
    Implementation of the Rabin-Karp string searching algorithm.
    """
    if not pattern:
        return 0
        
    # Prime number for modulo operations
    q = 101
    d = 256  # Number of characters in the alphabet
    
    n = len(text)
    m = len(pattern)
    
    if m > n:
        return -1
    
    # Calculate hash values for the pattern and the first window of text
    pattern_hash = 0
    text_hash = 0
    h = pow(d, m - 1) % q
    
    for i in range(m):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % q
        text_hash = (d * text_hash + ord(text[i])) % q
    
    # Slide the pattern over text one by one
    for i in range(n - m + 1):
        # Check if the hash values match
        if pattern_hash == text_hash:
            # Verify each character
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            
            if match:
                return i
        
        # Calculate hash value for the next window
        if i < n - m:
            text_hash = (d * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % q
            
            # Convert to positive value
            if text_hash < 0:
                text_hash += q
    
    return -1  # Pattern not found

def read_file(file_path):
    """
    Read a text file and return its content.
    Try different encodings if UTF-8 fails.
    """
    encodings = ['utf-8', 'cp1251', 'latin1', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    
    print(f"Error: Could not read {file_path} with any of the attempted encodings.")
    return ""

def measure_time(algorithm, text, pattern, number=10):
    """
    Measure execution time of a search algorithm.
    """
    setup_code = f"""
from __main__ import {algorithm.__name__}
text = {repr(text)}
pattern = {repr(pattern)}
"""
    stmt = f"{algorithm.__name__}(text, pattern)"
    times = timeit.repeat(stmt=stmt, setup=setup_code, number=number, repeat=5)
    return min(times) / number  # Return the best time

def format_time(seconds):
    """
    Format the time in appropriate units.
    """
    if seconds < 1e-6:
        return f"{seconds * 1e9:.4f} ns"
    elif seconds < 1e-3:
        return f"{seconds * 1e6:.4f} µs"
    elif seconds < 1:
        return f"{seconds * 1e3:.4f} ms"
    else:
        return f"{seconds:.4f} s"

def compare_algorithms(file1_path, file2_path):
    """
    Compare the performance of different string search algorithms on two text files.
    """
    # Read the text files
    text1 = read_file(file1_path)
    text2 = read_file(file2_path)
    
    if not text1 or not text2:
        print("Error reading one or both text files.")
        return
    
    # Define search patterns for each text
    # Existing patterns (found in the text)
    pattern1_existing = "algorithm"  # Assuming this exists in text1
    pattern2_existing = "research"   # Assuming this exists in text2
    
    # Non-existing patterns
    pattern1_fictional = "xyz123notfound"
    pattern2_fictional = "qwerty456notexist"
    
    algorithms = [boyer_moore_search, kmp_search, rabin_karp_search]
    results = {}
    
    # Test each algorithm with each pattern on each text
    for algo in algorithms:
        algo_name = algo.__name__.replace('_search', '')
        results[algo_name] = {}
        
        # Text 1, existing pattern
        time1_existing = measure_time(algo, text1, pattern1_existing)
        results[algo_name]['text1_existing'] = time1_existing
        
        # Text 1, fictional pattern
        time1_fictional = measure_time(algo, text1, pattern1_fictional)
        results[algo_name]['text1_fictional'] = time1_fictional
        
        # Text 2, existing pattern
        time2_existing = measure_time(algo, text2, pattern2_existing)
        results[algo_name]['text2_existing'] = time2_existing
        
        # Text 2, fictional pattern
        time2_fictional = measure_time(algo, text2, pattern2_fictional)
        results[algo_name]['text2_fictional'] = time2_fictional
    
    # Print results
    print("\nSearch Performance Comparison:\n")
    
    print(f"{'Algorithm':<15} {'Text 1 (Existing)':<20} {'Text 1 (Fictional)':<20} " +
          f"{'Text 2 (Existing)':<20} {'Text 2 (Fictional)':<20}")
    print("-" * 80)
    
    for algo_name, times in results.items():
        print(f"{algo_name:<15} {format_time(times['text1_existing']):<20} " +
              f"{format_time(times['text1_fictional']):<20} " +
              f"{format_time(times['text2_existing']):<20} " +
              f"{format_time(times['text2_fictional']):<20}")
    
    # Find the fastest algorithm for each case
    fastest_text1_existing = min(results.items(), key=lambda x: x[1]['text1_existing'])
    fastest_text1_fictional = min(results.items(), key=lambda x: x[1]['text1_fictional'])
    fastest_text2_existing = min(results.items(), key=lambda x: x[1]['text2_existing'])
    fastest_text2_fictional = min(results.items(), key=lambda x: x[1]['text2_fictional'])
    
    print("\nFastest Algorithms:")
    print(f"Text 1 (Existing pattern): {fastest_text1_existing[0]} - {format_time(fastest_text1_existing[1]['text1_existing'])}")
    print(f"Text 1 (Fictional pattern): {fastest_text1_fictional[0]} - {format_time(fastest_text1_fictional[1]['text1_fictional'])}")
    print(f"Text 2 (Existing pattern): {fastest_text2_existing[0]} - {format_time(fastest_text2_existing[1]['text2_existing'])}")
    print(f"Text 2 (Fictional pattern): {fastest_text2_fictional[0]} - {format_time(fastest_text2_fictional[1]['text2_fictional'])}")
    
    # Calculate overall performance
    for algo_name, times in results.items():
        results[algo_name]['overall'] = np.mean([
            times['text1_existing'],
            times['text1_fictional'],
            times['text2_existing'],
            times['text2_fictional']
        ])
    
    fastest_overall = min(results.items(), key=lambda x: x[1]['overall'])
    
    print(f"\nOverall fastest algorithm: {fastest_overall[0]} - {format_time(fastest_overall[1]['overall'])}")
    
    # Generate markdown report
    generate_report(results, file1_path, file2_path, pattern1_existing, pattern1_fictional, 
                   pattern2_existing, pattern2_fictional)

def generate_report(results, file1_path, file2_path, pattern1_existing, pattern1_fictional, 
                   pattern2_existing, pattern2_fictional):
    """
    Generate a report in markdown format with the comparison results.
    """
    with open("string_search_comparison.md", "w") as f:
        f.write("# String Searching Algorithms Performance Comparison\n\n")
        
        f.write("## Test Environment\n\n")
        f.write(f"- File 1: `{file1_path}`\n")
        f.write(f"- File 2: `{file2_path}`\n\n")
        
        f.write("### Search Patterns:\n\n")
        f.write("**Text 1:**\n")
        f.write(f"- Existing pattern: `{pattern1_existing}`\n")
        f.write(f"- Fictional pattern: `{pattern1_fictional}`\n\n")
        
        f.write("**Text 2:**\n")
        f.write(f"- Existing pattern: `{pattern2_existing}`\n")
        f.write(f"- Fictional pattern: `{pattern2_fictional}`\n\n")
        
        f.write("## Results\n\n")
        
        f.write("### Execution Times\n\n")
        f.write("| Algorithm | Text 1 (Existing) | Text 1 (Fictional) | Text 2 (Existing) | Text 2 (Fictional) | Overall |\n")
        f.write("|:----------|:-----------------|:-------------------|:------------------|:-------------------|:--------|\n")
        
        for algo_name, times in results.items():
            f.write(f"| {algo_name} | {format_time(times['text1_existing'])} | " +
                   f"{format_time(times['text1_fictional'])} | " +
                   f"{format_time(times['text2_existing'])} | " +
                   f"{format_time(times['text2_fictional'])} | " +
                   f"{format_time(times['overall'])} |\n")
        
        f.write("\n### Fastest Algorithms\n\n")
        
        fastest_text1_existing = min(results.items(), key=lambda x: x[1]['text1_existing'])
        fastest_text1_fictional = min(results.items(), key=lambda x: x[1]['text1_fictional'])
        fastest_text2_existing = min(results.items(), key=lambda x: x[1]['text2_existing'])
        fastest_text2_fictional = min(results.items(), key=lambda x: x[1]['text2_fictional'])
        fastest_overall = min(results.items(), key=lambda x: x[1]['overall'])
        
        f.write(f"- **Text 1 (Existing pattern)**: {fastest_text1_existing[0]} - {format_time(fastest_text1_existing[1]['text1_existing'])}\n")
        f.write(f"- **Text 1 (Fictional pattern)**: {fastest_text1_fictional[0]} - {format_time(fastest_text1_fictional[1]['text1_fictional'])}\n")
        f.write(f"- **Text 2 (Existing pattern)**: {fastest_text2_existing[0]} - {format_time(fastest_text2_existing[1]['text2_existing'])}\n")
        f.write(f"- **Text 2 (Fictional pattern)**: {fastest_text2_fictional[0]} - {format_time(fastest_text2_fictional[1]['text2_fictional'])}\n")
        f.write(f"- **Overall fastest algorithm**: {fastest_overall[0]} - {format_time(fastest_overall[1]['overall'])}\n\n")
        
        f.write("## Conclusion\n\n")
        f.write("Based on the performance measurements of the three string searching algorithms (Boyer-Moore, Knuth-Morris-Pratt, and Rabin-Karp) on two different texts with both existing and fictional patterns, we can observe:\n\n")
        
        # Determine which algorithm is generally best for each scenario
        if fastest_text1_existing[0] == fastest_text2_existing[0]:
            f.write(f"- For existing patterns, the **{fastest_text1_existing[0]}** algorithm consistently performs best across both texts.\n")
        else:
            f.write(f"- For existing patterns, performance varies: **{fastest_text1_existing[0]}** is fastest for Text 1, while **{fastest_text2_existing[0]}** is fastest for Text 2.\n")
        
        if fastest_text1_fictional[0] == fastest_text2_fictional[0]:
            f.write(f"- For fictional (non-existing) patterns, the **{fastest_text1_fictional[0]}** algorithm consistently performs best across both texts.\n")
        else:
            f.write(f"- For fictional patterns, performance varies: **{fastest_text1_fictional[0]}** is fastest for Text 1, while **{fastest_text2_fictional[0]}** is fastest for Text 2.\n")
        
        f.write(f"\nOverall, the **{fastest_overall[0]}** algorithm demonstrates the best average performance across all test cases. This suggests it would be the most reliable choice for general-purpose string searching tasks with unknown patterns and texts.\n")
        
        # Add algorithm-specific insights
        f.write("\n### Algorithm Characteristics\n\n")
        f.write("- **Boyer-Moore**: Generally performs well, especially for longer patterns, as it can skip portions of the text. Its performance advantage is more pronounced in cases where the pattern is not found or appears near the end of the text.\n")
        f.write("- **Knuth-Morris-Pratt**: Ensures linear time complexity in the worst case and performs consistently across different scenarios.\n")
        f.write("- **Rabin-Karp**: Uses hashing to efficiently handle multiple pattern searches, but may not always outperform the other algorithms for single pattern searches.\n")

if __name__ == "__main__":
    # Specify the paths to the text files
    article1_path = "article1.txt"  # Update with your actual file path
    article2_path = "article2.txt"  # Update with your actual file path
    
    # Run the comparison
    compare_algorithms(article1_path, article2_path)

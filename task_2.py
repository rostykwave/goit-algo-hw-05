def binary_search(arr, target):
    """
    Perform binary search on a sorted array of floating point numbers.
    
    Args:
        arr: A sorted array of floating point numbers.
        target: The value to search for.
    
    Returns:
        A tuple where the first element is the number of iterations,
        and the second element is the upper bound (smallest element
        greater than or equal to the target value).
    """
    iterations = 0
    
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return (iterations, arr[mid])
        elif arr[mid] < target:
            left = mid + 1
        else:  # arr[mid] > target
            right = mid - 1
    
    # If the element was not found, return the upper bound
    if left < len(arr):
        return (iterations, arr[left])
    else:
        return (iterations, None)  # No upper bound exists

# Test cases
if __name__ == "__main__":
    arr = [0.1, 1.2, 2.3, 3.4, 4.5, 5.6, 6.7, 7.8, 8.9, 9.0]
    
    # Test case 1: Element exists in the array
    print(binary_search(arr, 4.5))  # Should return the element with iterations
    
    # Test case 2: Element doesn't exist, but there's an upper bound
    print(binary_search(arr, 4.0))  # Should return 4.5 as upper bound
    
    # Test case 3: Element is less than all elements in the array
    print(binary_search(arr, 0.0))  # Should return 0.1 as upper bound
    
    # Test case 4: Element is greater than all elements in the array
    print(binary_search(arr, 10.0))  # Should return None as upper bound

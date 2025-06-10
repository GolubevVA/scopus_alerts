import functools

def flaky_passes(min_passes: int = 3, runs: int = 5):
	'''
	Decorator to retry a test function multiple times (`runs` times) until it passes a minimum number of time (`min_passes` times).
	'''
	def decorator(test_func: callable):
		@functools.wraps(test_func)
		async def wrapper(*args, **kwargs):
			passes = 0
			fails = 0
			for _ in range(runs):
				try:
					await test_func(*args, **kwargs)
					passes += 1
				except Exception:
					fails += 1
				if passes >= min_passes:
					break
				if runs - fails < min_passes:
					raise Exception(f"Test failed {fails} times out of {runs} runs for {test_func.__name__}.")
			assert passes >= min_passes, f"Test passed only {passes} out of {runs} times for {test_func.__name__}."
		return wrapper
	return decorator

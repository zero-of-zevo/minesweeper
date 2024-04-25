# Import required modules
import numpy as np

# Directional Arrays
dx = [-1, 0, 1, -1, 0, 1, -1, 0, 1]
dy = [0, 0, 0, -1, -1, -1, 1, 1, 1]

# Function to check if the cell (x, y) is valid or not
def isValid(x, y, N, M):
	return (x >= 0 and y >= 0 and x < N and y < M)

# Function to print the matrix grid[][]
def printGrid(grid):
	for row in grid:
		for cell in row:
			if cell:
				print("x", end=" ")
			else:
				print("_", end=" ")
		print()

# Function to check if the cell (x, y) is valid to have a mine or not
def isSafe(arr, x, y, N, M):
	# Check if the cell (x, y) is a valid cell or not
	if not isValid(x, y, N, M):
		return False

	# Check if any of the neighbouring cell of (x, y) supports (x, y) to have a mine
	for i in range(9):
		if isValid(x + dx[i], y + dy[i], N, M) and (arr[x + dx[i]][y + dy[i]] - 1 < 0):
			return False

	# If (x, y) is valid to have a mine
	for i in range(9):
		if isValid(x + dx[i], y + dy[i], N, M):
			# Reduce count of mines in the neighboring cells
			arr[x + dx[i]][y + dy[i]] -= 1

	return True

# Function to check if there exists any unvisited cell or not
def findUnvisited(visited):
	for x in range(len(visited)):
		for y in range(len(visited[0])):
			if not visited[x][y]:
				return x, y
	return -1, -1

# Function to check if all the cells are visited or not and the input array is satisfied with the mine assignments
def isDone(arr, visited):
	done = True
	for i in range(len(arr)):
		for j in range(len(arr[0])):
			done = done and (arr[i][j] == 0) and visited[i][j]
	return done

# Function to solve the minesweeper matrix
def SolveMinesweeper(grid, arr, visited, N, M):
	# Function call to check if each cell is visited and the solved grid is satisfying the given input matrix
	done = isDone(arr, visited)

	# If the solution exists and all cells are visited
	if done:
		return True

	x, y = findUnvisited(visited)

	# Function call to check if all the cells are visited or not
	if x == -1 and y == -1:
		return False

	# Mark cell (x, y) as visited
	visited[x][y] = True

	# Function call to check if it is safe to assign a mine at (x, y)
	if isSafe(arr, x, y, N, M):
		# Mark the position with a mine
		grid[x][y] = True

		# Recursive call with (x, y) having a mine
		if SolveMinesweeper(grid, arr, visited, N, M):
			# If solution exists, then return true
			return True

		# Reset the position x, y
		grid[x][y] = False
		for i in range(9):
			if isValid(x + dx[i], y + dy[i], N, M):
				arr[x + dx[i]][y + dy[i]] += 1

	# Recursive call without (x, y) having a mine
	if SolveMinesweeper(grid, arr, visited, N, M):
		# If solution exists then return true
		return True

	# Mark the position as unvisited again
	visited[x][y] = False

	# If no solution exists
	return False

# Function to perform generate and solve a minesweeper
def minesweeperOperations(arr, N, M):
	# Stores the final result
	grid = np.zeros((N, M), dtype=bool)

	# Stores whether the position (x, y) is visited or not
	visited = np.zeros((N, M), dtype=bool)

	# If the solution to the input minesweeper matrix exists
	if SolveMinesweeper(grid, arr, visited, N, M):
		# Function call to print the grid[][]
		printGrid(grid)
	# No solution exists
	else:
		print("No solution exists")

# Driver Code
if __name__ == "__main__":
	# Given input
	N = 7
	M = 7
	arr = [
		[1, 1, 0, 0, 1, 1, 1],
		[2, 3, 2, 1, 1, 2, 2],
		[3, 5, 3, 2, 1, 2, 2],
		[3, 6, 5, 3, 0, 2, 2],
		[2, 4, 3, 2, 0, 1, 1],
		[2, 3, 3, 2, 1, 2, 1],
		[1, 1, 1, 1, 1, 1, 0]
	]

	# Function call to perform generate and solve a minesweeper
	minesweeperOperations(arr, N, M)

import tkinter as tk
import time
import random
from heapq import heapify, heappop

width, height = 1100, 700
buttonW, buttonH = .1, .05
size = 20
vals = [None] * size
bars = [None] * size
sortSpeed = 300
interrupt = False
sorting = False
defaultColor = 'RoyalBlue'
selectColor = 'magenta2'
currTime = 0
mergeQueue = []
quickQueue = []

root = tk.Tk()
root.title("Sorting Visualization")

canvas = tk.Canvas(root, height = height, width = width, bg = 'pale green')
canvas.pack()

def shiftRight(indices): 
	global vals
	for i in indices:
		vals[i] = vals[i - 1]

def mergeAnimation(newStep = True, positions = False, prev = None, newComparison = True): 
	global interrupt, sorting, vals, mergeQueue
	if (not mergeQueue and not positions) or interrupt:
		buttonColor(merge, False)
		interrupt = False
		sorting = False
		mergeQueue = []
		return

	if newStep:
		positions = mergeQueue.pop(0)
	if newComparison:
		left, right = positions[0], positions[1]
		lstart, rstart = positions[2], positions[3]
		changeColor(prev, defaultColor) if type(prev) == int else False
		changeColor(lstart, selectColor) if left else False
		changeColor(rstart, selectColor) if right else False
		scalingSpeed = 0 if size >= 200 and sortSpeed <= 1 else sortSpeed
		root.after(scalingSpeed, lambda: mergeAnimation(False, positions, None, False))
	else:
		left, right = positions[0], positions[1]
		lstart, rstart = positions[2], positions[3]
		if left and right:
			if left[0] < right[0]:
				left = left[1:]
				lstart += 1
				changeColor(rstart, defaultColor)
			elif left[0] == right[0]:
				changeColor(lstart, defaultColor)
				changeColor(rstart, defaultColor)
				left = left[1:]
				lstart += 1
			else:
				temp = vals[rstart]
				shiftRight(range(rstart, lstart, -1))
				vals[lstart] = temp
				updateScreen()

				right = right[1:]
				rstart += 1
				lstart += 1
				changeColor(lstart - 1, selectColor)
		elif left:
			changeColor(lstart, defaultColor)
			lstart += 1
			left = left[1:]
		elif right:
			changeColor(rstart, defaultColor)
			rstart += 1
			right = right[1:]

		if left or right:
			positions[0], positions[1], positions[2], positions[3] = left, right, lstart, rstart
			root.after(sortSpeed, lambda: mergeAnimation(False, positions, lstart - 1))
		else:
			root.after(sortSpeed, lambda: mergeAnimation(True))

def mergeCombine(left, right): 
	combined = []
	while left and right:
		if left[0] <= right[0]:
			combined.append(left[0])
			left = left[1:]
		else:
			combined.append(right[0])
			right = right[1:]
	if left:
		combined += left
	elif right:
		combined += right
	return combined

def merge(lst = None, newSort = True, start = 0, end = 0): 
	global sorting
	if sorting and newSort: 
		return
	elif newSort:
		sorting = True
		buttonColor(merge, True)
		end = size 
	lst = vals if not lst else lst

	
	length = len(lst)
	if length == 1:
		return lst
	middle = length // 2 if length % 2 == 0 else length // 2 + 1
	left = merge(lst[: middle], False, start, middle)
	right = merge(lst[middle:], False, start + middle, end)
	lst = mergeCombine(left, right) 
	mergeQueue.append([left, right, start, start + middle]) 

	if len(lst) == len(vals): 
		mergeAnimation()
	else:
		return lst



def selection(start = 0, newSort = True, iteration = 0, currMin = float('inf'), minIdx = None): 
	global interrupt, sorting
	if sorting and newSort: 
		return
	elif newSort:
		sorting = True
		buttonColor(selection, True)
	if start == size or interrupt: 
		changeColor(start - 1, defaultColor)
		interrupt = False
		sorting = False
		buttonColor(selection, False)
		return
	

	
	if iteration % 2 == 0: 
		changeColor(start - 1, defaultColor) if start != 0 else None
		for i in range(start, size):
			if vals[i] < currMin:
				currMin = vals[i]
				minIdx = i
		changeColor(minIdx, selectColor)
		root.after(sortSpeed, lambda: selection(start, False, iteration + 1, currMin, minIdx))
		
	else:
		clearRectangles([minIdx, start])
		swap(start, minIdx)
		drawRect(start, selectColor)
		drawRect(minIdx, defaultColor)
		root.after(sortSpeed, lambda: selection(start + 1, False))
		

def swap(index1, index2):
	vals[index1], vals[index2] = vals[index2], vals[index1]

def changeColor(index, color):
	canvas.itemconfig(bars[index], fill = color, outline = color)

def drawRect(i, color):
	barWidth = (width * 0.9) / size
	startX = width * 0.05
	endY = height * 0.885

	x1 = startX + i * barWidth
	y1 = endY - (vals[i] / (size * 10)) * (.8 * height)
	x2 = x1 + barWidth
	bars[i] = canvas.create_rectangle(x1, y1, x2, endY, fill = color, outline = color, tag = 'rect')

def clearRectangles(lst):
	if not lst:
		canvas.delete('rect')
	else:
		for index in lst:
			canvas.delete(bars[index])

def updateScreen():
	global bars
	clearRectangles(None) 
	bars = [None] * size
	for i in range(size):
		drawRect(i, defaultColor)		

def randomVals():
	global vals
	random.seed(time.time())
	vals = [None] * size
	for i in range(size):
		vals[i] = random.randint(1, size * 10)
	updateScreen()

def changeSize(newSize):
	global size, interrupt
	interrupt = True if sorting else False
	size = int(newSize)
	randomVals()

def buttonColor(algorithm, pressed):
	index = funcs.index(algorithm)
	buttons[index]['highlightbackground'] = 'snow4' if pressed else 'white'

def slow():
	global sortSpeed
	sortSpeed = 300
	speedButton[0]['highlightbackground'] = 'snow4'
	speedButton[1]['highlightbackground'] = 'white'
	speedButton[2]['highlightbackground'] = 'white'

def medium():
	global sortSpeed
	sortSpeed = 70
	speedButton[0]['highlightbackground'] = 'white'
	speedButton[1]['highlightbackground'] = 'snow4'
	speedButton[2]['highlightbackground'] = 'white'

def fast():
	global sortSpeed
	sortSpeed = 1
	speedButton[0]['highlightbackground'] = 'white'
	speedButton[1]['highlightbackground'] = 'white'
	speedButton[2]['highlightbackground'] = 'snow4'


sorts = ["Merge Sort", "Selection Sort"]
funcs = [merge, selection]
modes = ["Slow", "Medium", "Fast"]
speeds = [slow, medium, fast]
buttons = []
speedButton = []

for i in range(len(sorts)): 
	buttons.append(tk.Button(canvas, text = sorts[i], command = funcs[i]))
	buttons[i].place(relx = 0.005 * (i + 1) + buttonW * i, rely = 0.005, relwidth = buttonW, relheight = buttonH)

inputSize = tk.Scale(canvas, from_ = 10, to = 1000, tickinterval = 90, orient = tk.HORIZONTAL, bg = 'light blue', command = changeSize)
inputSize.place(relx = 0.5 - buttonW * 4.5, rely = 1 - buttonH * 2.1, relwidth = buttonW * 6, relheight = buttonH * 2)
inputSize.set(size)

randomize = tk.Button(canvas, text = 'Reset', command = lambda: changeSize(size))
randomize.place(relx = 1 - buttonW * 1.1, rely = 0.005, relwidth = buttonW, relheight = buttonH)

for i in range(3): 
	speedButton.append(tk.Button(canvas, text = modes[i], command = speeds[i]))
	speedButton[i].place(relx = 0.5 + 1.75 * buttonW + buttonW * i, rely = 1 - buttonH * 1.55, relwidth = buttonW, relheight = buttonH)

randomVals()
slow()
root.mainloop()


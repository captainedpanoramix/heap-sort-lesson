#heapsortdebug.py
# debug stuff
import math
myBT=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
sp4=" " # really only 1
sp8="     " # really only 5
sp16="             " # really only 13
sp32="                             " # really only 29

def pR1(a):
	print (sp32,a[0])
def pR2(a):
	print (sp16,a[1],sp32,a[2])
def pR3(a):
	print(sp8,a[3],sp16,a[4],sp16,a[5],sp16,a[6],sp16)
def pR4(a):
	print(sp4,a[7],sp8,a[8],sp8,a[9],sp8,a[10],sp8,a[11],sp8,a[12],sp8,a[13],sp8,a[14])
def pR(a): # this prints the whole array, as a binary tree (without lines)
	pR1(a)
	pR2(a)
	pR3(a)
	pR4(a)

#pR(myBT)


#-------------------------------
def iParent(i):
	return math.floor((i-1)/2)

def iLeftChild(i):
	return 2*i+1
def iRightChild(i):
	return 2*i+2

def swapAndDrop( a, start, end):
	# start make this node obey the invariant
	# end is the last node in the list, any larger number is not a node.
	# print("SwapandDrop, start=",start)

	node = start # eventually we might swap node with swap
	while iLeftChild(node) <= end:
		#
		# print("Inspecting node",node, "=",a[node])
		swap = node # if they are the same down below, no swap.
		if a[node] < a[iLeftChild(node)] : 
			swap = iLeftChild(node)  # be ready to swap with left child
		if iRightChild(node) <= end and a[swap] < a[iRightChild(node)] : 
			swap = iRightChild(node) # but if right child is larger, prepare for right child
		if swap == node : # invariant is already obeyed below here
			return
		else : # need to swap and drop down to the child
			# print( "---swapping ",node,", ",a[node]," with ",swap, "swap, ",a[swap])
			a[node],a[swap] = a[swap],a[node] 
			node = swap # drop down and try again

def createMaxHeap ( a, count):
# change the list a into a list that embodies a binary tree that obeys the heap invariant.
# There are  count items in the list
# Starting with the rightmost parent node, visit each node in order towards the root, imposing the heap invariant on each one.
	start = iParent(count-1) # count-1 is the last leaf in the tree. No largerindex numbers should exist.
	while start >= 0:
		swapAndDrop( a, start, count-1)
		start = start -1

#myBT=['O','N','M','L','K','J','I','H','G','F','E','D','C','B','A']
#myBT=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
myBT=[43,26,31,24,15,12,11,18,19,9,13,17,28,2,7]
print(myBT)
pR(myBT)
print("===============next CreateMaxHeap")
createMaxHeap(myBT,15)

pR(myBT)

print("===============next CreateMaxHeap")

def fetchMaxHeap( a, count ):
	end = count - 1 # subscript of last leaf, repurposed to be subscript of highest value in sorted array.
	while end > 0:
		a[end],a[0] = a[0],a[end] # swap(a[end], a[0])
		end = end - 1
		swapAndDrop( a, 0, end) # we destroyed the invariance, so correct it, which will locate the highest remaining value and place it in a(0)

fetchMaxHeap (myBT,15)
print (myBT)

def genFetchMaxHeap( a, count ): # the iterator for a heap
	end = count - 1 # subscript of last leaf, repurposed to be subscript of highest value in sorted array.
	while end >= 0:
		yield a[0]
		a[end], a[0]=a[0],a[end]
		end = end - 1
		swapAndDrop( a, 0, end)
#---do it all over again, with generator fetching instead
#myBT=['O','N','M','L','K','J','I','H','G','F','E','D','C','B','A']
#myBT=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
myBT=[43,26,31,24,15,12,11,18,19,9,13,17,28,2,7]
print(myBT)
pR(myBT)
print("===============next CreateMaxHeap")
createMaxHeap(myBT,15)
pR(myBT)
print ("as a generator")

fetcher=genFetchMaxHeap(myBT,15)
for i in range(15):
	print(next(fetcher))


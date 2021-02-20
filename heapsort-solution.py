import math	# needed for floor function


# debug stuff

# ------------------ components of pR() debug print function
sp4="   " # really only 1
hy4="-"
sp8="    " # really only 5
hy8="----"
sp16="              " # really only 14
sp14="            "
hy16="-----------"
sp18="             "
sp32="                             " # really only 29
hy32="---------------------------"

def pR1(a):
	print (sp32,a[0])
def pR2(a):
	print (sp16,a[1],hy32,a[2])
def pR3(a):
	print("       ",a[3],hy16,a[4],sp14,a[5],hy16,a[6],sp16)
def pR4(a):
	print(sp4,a[7],hy8,a[8],sp8,a[9],hy8,a[10],sp8,a[11],hy8,a[12],sp8,a[13],hy8,a[14])
def pR(a): # this prints the whole array, as a binary tree (with lines connecting siblings and parent)
	pR1(a)
	pR2(a)
	pR3(a)
	pR4(a)
# ----------------- end of pR()

#================ components of heapsort
# 
# These routines embed a binary tree in a simple Python list. This embedding is called a "heap"
# There are no explicit links between nodes, instead parentage is inferred from location in the list
# The root of the tree is the item at index 0
# The children of the root are the items at index 1:2
# In fact, the children of a node at index i are located at (2*i + 1) and  (2*i + 2)
# Conversely, the parent of a node at index i is located at ( floor((i-1)/2) )

# This file includes a crude debug print function called pR(a) for a heap with 15 nodes
# 
def iParent(i):
	return math.floor((i-1)/2)

def iLeftChild(i):
	return 2*i+1
def iRightChild(i):
	return 2*i+2

def swapAndDrop( a, start, end):
	# makes a node obey the invariant
	# start -- index of node to process 
	# end -- index of the last node in the list, any larger number is not a node.

	node = start # eventually we might swap node with swap
	while iLeftChild(node) <= end:
		swap = node # if they are equal down below, don't swap.
		if a[node] < a[iLeftChild(node)] : 
			swap = iLeftChild(node)  # be ready to swap with left child
		if iRightChild(node) <= end and a[swap] < a[iRightChild(node)] : 
			swap = iRightChild(node) # but if right child is larger, prepare for right child
		if swap == node : # invariant is already obeyed below here, or there are no children
			return
		else : # need to swap and drop down to the child
			a[node],a[swap] = a[swap],a[node]  
			node = swap # drop down and try again

def createMaxHeap ( a, count):
	# Change the list a into a list that embodies a binary tree that obeys the heap invariant.
	# The HEAP INVARIANT is that each node's value is greater than that of its child(ren)
	# a -- entire list
	# count -- number of items in the list 
	# Starting with the rightmost parent node, visit each node in order towards the root, imposing the heap invariant on each one.
	# There is no need to call swapAndDrop on the leaves, as they are trivially compliant, as they have no children
	# Therefore, this routine starts by locating the rightmost leaf, and stepping back to its parent.
	start = iParent(count-1) # count-1 is the index of the last leaf in the tree. No largerindex numbers should exist.
	while start >= 0:
		swapAndDrop( a, start, count-1)
		start = start -1

def fetchMaxHeap( a, count ):
	# Floyd's implement of fetch. Each iteration of the while statement removes the top node from the tree 
	# and places it at the head of the sorted sublist.
	# Ingeniously, the "remaining tree" and the "unsorted sublist" share the space of the original list
	# So, in general, a[0:end] is the remaining tree, while a[end:] is the array, sorted in ascending order
	end = count - 1 # subscript of last leaf, repurposed to be subscript of highest value in sorted array.
	while end > 0:
		a[end],a[0] = a[0],a[end] # swap(a[end], a[0])
		end = end - 1
		swapAndDrop( a, 0, end) # we destroyed the invariance, so correct it, 
			# which will locate the highest remaining value and place it in a(0)
	# When the call to fetchMaxHeap is complete, the tree is gone, and a[:] is the entire list, in ascending order


def genFetchMaxHeap( a, count ): 
	# variant of Floyd's algorithm, that performs as a Python generator
	# that iteratively yields the root (largest node remaining) to the caller
	end = count - 1 # subscript of last leaf, repurposed to be subscript of highest value in sorted array.
	while end >= 0:
		yield a[0] # This is the only Python statement that makes this a generator.
		a[end], a[0]=a[0],a[end]
		end = end - 1
		swapAndDrop( a, 0, end)

# ==================================== end of heap sort routines
# ==================================== begin of demonstration code

# sample lists of length 15. The main routines can handle much longer lists, but the debug routine crudely assumes only 15

#myBT=['O','N','M','L','K','J','I','H','G','F','E','D','C','B','A']
#myBT=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
#myBT=[43,26,31,24,15,12,11,18,19,9,13,17,28,2,7]

myBT=[15,18,31,24,43,12,11,26,19,9,13,17,28,2,7]
print ("Beginning list")
print(myBT) # simply print the list
print ("List as a binary tree")
pR(myBT) # display the list as a binary tree

createMaxHeap(myBT,15) #<------ Phase 1: create heap
print ("List modified to obey heap invariant")

pR(myBT) # display the list as a heap (binary tree obeying the heap invariant)
fetchMaxHeap(myBT,15) #<------  Phase 2: sort heap in place

print ("List, sorted ascending")
print(myBT) # print the list and see that it is sorted in ascending order.

# -------------- Same demonstration, but exercise the generator
print ("Same demonstration, exercising the generator")
myBT=[15,18,31,24,43,12,11,26,19,9,13,17,28,2,7]
print ("Beginning list")
print(myBT) # simply print the list
print ("List as a binary tree")
pR(myBT) # display the list as a binary tree

createMaxHeap(myBT,15) # ------ Phase 1: create heap
print ("List modified to obey heap invariant")
pR(myBT)

print ("fetch root nodes as they appear, in descending order")
fetcher=genFetchMaxHeap(myBT,15) # fetcher is now a generator/iterator
for i in range(15):
	print(next(fetcher)) 
# The loop printed the items in descending order
# By the way, the myBT list is still the list in ascending order.

print ("List is in ascending order")
print (myBT)

# ====================================== end of demonstration code
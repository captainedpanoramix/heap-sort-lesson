# Heapsort #
One of the most efficient sorting algorithms is called "heapsort". It uses a special concept called a "heap", and proceeds in two phases. The first phase creates a heap from an ordinary list, and the second phase transforms that heap into a sorted list. This lesson shows how to code each of these, as well as a modification of the second phase that reads the sorted data directly out of the heap.
## Structure of Heap ##
A heap is a manifestation of a binary tree (each internal node has no more than two children) that obeys the "heap invariant."
### Heap implementation###
Store the items as a binary tree in a linear array, root first, first generation descendants next, second gen descendants next, etc. This table shows a random list (the row called "value"), and how they are related in a binary tree. The pedigree explains the tree relationships. Node A has children AA and AB; node AA has children AAA and AAB, while node AB has children ABA and ABB, and so on. 


Index	|0	|1	|2	|3	|4	|5	|6	|7	|8	|9	|10	|11|12	|13	|14
---:---:---:---:---:---:---:---:---:---:---:---:---:---:---:---
Pedigree	|A	|AA	|AB	|AAA	|AAB	|ABA	|ABB	|AAAA	|AAAB	|AABA	|AABB	|ABAA	|ABAB	|ABBA|ABBB
value	|17	|43	|12	|19	|13	|28	|7	|18	|24	|9	|15	|26	|31	|2	|11

####Location of parent####
If child node is at index "i", the parent is at "floor((i-1)/2)". For example, item 10 (AABB, with value 15) has its parent at "floor((10-1)/2)" = "floor(9/2)" = 4 with pedigree AAB.
####Location of child####
If a parent node is at index "i", the left child is at "2*i + 1", right child at "2*i + 2". For example, the node at index "2" (AA, with value 43) has children 2*2+1=5 (ABA) and 2*2+2=6(ABB) .


Notice the children of a parent are adjacent to each other.	


### Heap constraint / invariant###
The heap invariant is that each node in the tree must have a higher value than any of its children. 
Notice that values close together are NOT necessarily close together in the tree.

Because this array properly obeys the heap invariant, it qualifies as a heap.
Index	|0	|1	|2	|3	|4	|5	|6	|7	|8	|9	|10	|11	|12	|13	|14
---:---:---:---:---:---:---:---:---:---:---:---:---:---:---:---
Pedigree|A	|AA	|AB	|AAA	|AAB	|ABA	|ABB	|AAAA	|AAAB|	AABA	|AABB	|ABAA	|ABAB	|ABBA|	ABBB
value	|43	|26	|31	|24	|15	|28	|11	|18	|19	|9	|13	|17	|12	|2	|7

For example, see that A contains 43, its children AA and AB contain 26 and 31. Their children AAA and AAB are 24 and 15, and ABA and ABB are 12 and 11, and so on.

##First phase--Constructing a heap (createMaxHeap)##

The function "createMaxHeap" takes a list, and changes the list to represent a binary tree that obeys the heap invariant. Its main subfunction imposes the heap invariance on all of the parent nodes in the tree. Let’s understand it first.
The approach uses a function "swapAndDrop" that imposes the heap invariant on all the nodes. It operates bottom-up. That is, it is called on bottom level parent nodes first, so that every time it is called for a node, it can assume that the node’s children’s trees already obey the invariant. The function does whatever is necessary to ensure that the node itself also obeys the invariant.


What is the key operation? 
*	Examine a node and its immediate children. 
*	If a child is larger than the node, swap the node with its larger child.

Moving the larger child to the node’s position is consistent with the heap invariant, because it is guaranteed to be larger than both of its children.

However, moving the (smaller) node to the child’s position may break the invariant, because this lower value might NO LONGER be larger than its children. As a result, if swapping happens, the routine needs to drop down and inspect the child as well. Therefore, this routine is called "swapAndDrop".
While this functional description is complete, there is more bookkeeping to do. Since the routine can loop downward in the tree, how and when does it stop?
It will stop when the value of "node" is indeed larger than that of its children, or if it doesn’t even have children. There are no children if the "iLeftChild" or "iRightChild" functions return a value greater than the "end" argument.

Pseudocode:
```
Procedure swapAndDrop( a, start, end)
	# start is the index of the node that might not obey the invariant 
	# end is the index of the last node in the list, any larger number is not a node.
	node = start # eventually we might swap node with swap
	while iLeftChild(node) <= end do
		swap = node # if they are the same down below, no swap.
		If a[node] < a[iLeftChild(node)]  then swap = iLeftChild(i)  # be ready to swap with left child
		If iRightChild(node) <= end and a[node] < a[iRightChild(i)] then 
			swap = iRightChild(i) # but if right child is larger, prepare for right child
		If swap == node then # invariant is already obeyed below here
			Return
		Else # need to swap and drop down to the child
			swap a[node] with a[swap]
			node = swap # drop down and try again
```

Now we can express the main creation routine.


Pseudocode:

```
Procedure createMaxHeap ( a, count)
# change the list a into a list that embodies a binary tree that obeys the heap invariant.
# There are  count items in the list
# Starting with the rightmost parent node, visit each node in order towards the root, imposing the heap invariant on each one.
	start = iParent(count-1) # count-1 is the last leaf in the tree. No larger index numbers should exist.
	while start >= 0
		swapAndDrop( a, start, count-1)
		start = start -1
```
Once createMaxHeap is complete, the array a represents a binary tree that behaves the heap invariant.




##Fetching the items in order##
Here are two ways to fetch the items in descending order. The original optimal form of this algorithm, invented by R. W. Floyd, has the beautiful property that it iteratively shrinks the tree by removing its largest values and placing them at the end of the array. In other words, it can sort the array in place, in ascending order. This allows the items to be accessed in either ascending or descending order. Also, numerical values can be divided into quartiles, deciles, percentiles, etc. 

Another approach, inspired by Python’s generator concept, iteratively removes the values from largest to smallest and returns them, one at a time, to a calling routine.
Both methods use the swapAndDrop routine.
The algorithm maintains the shrinking tree in lower cells, and grows the sorted list in higher cells. At the beginning, the tree occupies all count-1 cells, and there is no sorted list. The function swaps the largest value (located in a(0)) with the last leaf in the tree (located in a[count-1]). This starts the sorted list and shrinks the tree by the removal of that last leaf. By swapping it into a[0], the function breaks the heap invariance, so it calls swapAndDrop to repair the tree by sliding the low value downward and the highest value upward. Now, a[0] is the highest remaining value, and the last leaf in the tree is located in a[count-2]. This swapping and swapAndDropping proceeds until the tree portion is shrunk to nothing, and the ascending sorted items fill the array.
###Floyd's algorithm###
```
Pseudocode:
Procedure fetchMaxHeap( a, count )
	End = count - 1 # subscript of last leaf, repurposed to be subscript of highest value in sorted array.
	While end > 0
		Swap a[end] with a[0]
		End = end - 1
		swapAndDrop( a, 0, end) # we destroyed the invariance, so correct it, which will locate the highest remaining value and place it in a(0)
	# At this point, the entire array is in ascending order. Play with it as you wish!
```

###Python generator form###

Essentially the same, but it yields a[0] at each call, so it produces the array in descending order.

```
Pseudocode:
Procedure genFetchMaxHeap( a, count ) # the iterator for a heap
	end = count - 1 # subscript of last leaf, repurposed to be subscript of highest value in sorted array.
	while end >= 0
		yield a[0]
		Swap a[end] with a[0]
		end = end - 1
		swapAndDrop( a, 0, end) # we destroyed the invariance, so correct it, which will locate the highest remaining value and place it in a(0)
	# At this point, the entire array is in ascending order. Play with it as you wish!
```
To use this generator
```python
fetcher=genFetchMaxHeap(a,15)
for i in range(15):
	print(next(fetcher))
```

import re
import string
import itertools
import numpy as np
import sys

def calculateBestResponse(profile):
	#print "Calc Best Resp"
	#print profile
	currPlayer=profile.index(-1)
	maxPayOff=utils[currPlayer][utils[currPlayer].keys()[0]]
	for k in range(1,stratergies[currPlayer]+1):
		curr_util = utils[currPlayer][tuple(profile[:currPlayer]+[k]+profile[currPlayer+1:])]
		if curr_util > maxPayOff:
			maxPayOff = curr_util
	bestResponse=[]
	for k in range(1,stratergies[currPlayer]+1):
		curr_util = utils[currPlayer][tuple(profile[:currPlayer]+[k]+profile[currPlayer+1:])]
		if curr_util == maxPayOff:
			bestResponse.append(k)
	bestResponseMap[tuple(profile)] = bestResponse


def printIfBestResponse(profile):
	for j in range(0,len(stratergies)):
		currPlayer = j
		if profile[j] not in bestResponseMap[tuple(profile[:currPlayer]+[-1]+profile[currPlayer+1:])]:
			return
	#print "--------------------------"
	print tuple(profile)


# function for claculating cartesian product of vectors
def cartesian(arrays, out=None):
    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype

    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)

    m = n / arrays[0].size
    out[:,0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m,1:])
        for j in xrange(1, arrays[0].size):
            out[j*m:(j+1)*m,1:] = out[0:m,1:]
    return out

# opening file
f=open(sys.argv[1],"r")
count=0
line=[]
ll=[]
for i in f:
    if i!='\n':
        ll+=i
	line+=[i]
chars=[]
for i in ll:
    if i!=' ' and i!='\n':
        chars+=i
ct=0
ct1=0
mark=-1
mark1=-1
for i in range(len(chars)):
    if chars[i]=='{':
        ct+=1
        if ct==2:
            mark=i+1
    if chars[i]=='}':
        ct1+=1
        if ct==2:
            mark1=i+1
k=mark
strat=[]
while 1:
    if(chars[k]=='}'):
        break
    strat+=[int(chars[k])]
    k+=1

nums=[]
k=mark1
flag=0
temp1=line[1].split()
for i in temp1:
	nums+=[float(i)]
count=len(strat)


# calculating indiviual player utilities
num_p=[[]]*count
k=0
for i in range(len(num_p)):
    k=i
    temp_num=[]
    while(k<len(nums)):
        temp_num+=[nums[k]]
        k=k+count
    num_p[i]=temp_num
b=[]
c1=-1
player=[{}]*count
arr=[[]]*count
for i in range(len(strat)):
    temp=[]
    for j in range(strat[i]):
        temp+=[j+1]
    arr[i]=temp
arr.reverse()
arr=tuple(arr)



# creating dictionary for storing utlities
c=cartesian(arr)
ans=[]
for i in range(len(c)):
    k=tuple(c[i])
    ans+=(k,)
it=0
# print ans
for i in range(len(player)):
    temp={}
    for j in range(len(ans)):
        temp.update({ans[j]:num_p[i][j]})
    player[i]=temp

# print player


utils=[]
for play in player:
	final={}
	for key in play:
		final[key[::-1]]=play[key]
	utils.append(final)

print utils
stratergies=strat
bestResponseMap={}
#####################################################################


# player list contains dictionaries of all players
# example : player=[{(1, 2): 0, (1, 3): 0, (2, 3): 2, (2, 2): 0, (1, 1): 1, (2, 1): 1},
#        {(1, 2): 2, (1, 3): 2, (2, 3): 0, (2, 2): 3, (1, 1): 1, (2, 1): 1}]
# player[0][1,2] => for player 0 ,key is (1,2) and utility is 0
# (1,2)=>strategy of player 1 is 2 and player 2 is 1

#####################################################################

# claculating equilibrium
### /*

# insert code here
for j in range(0,len(stratergies)):
	#print "Player "+str(j+1)
	currPlayer = j
	curr = [1 for i in range(0,len(stratergies))]
	curr[currPlayer]=-1
	while (curr[:currPlayer]+curr[currPlayer+1:]) != (stratergies[:currPlayer]+stratergies[currPlayer+1:]):
		calculateBestResponse( curr)
		for i in range(0,len(stratergies)):
				if i == currPlayer:
					continue
				curr[i]=curr[i]+1
				if curr[i] > stratergies[i]:
						curr[i]=1
				else:
						break
	calculateBestResponse(curr)

#print bestResponseMap


#Finally output pure stratergy equilibrium

curr = [1 for i in range(0,len(stratergies))]
while stratergies != curr:
    printIfBestResponse(curr)
    for i in range(0,len(stratergies)):
            curr[i]=curr[i]+1
            if curr[i] > stratergies[i]:
                    curr[i]=1
            else:
                    break

printIfBestResponse(curr)


### */
#closing file

f.close()

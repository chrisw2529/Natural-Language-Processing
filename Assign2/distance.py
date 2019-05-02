# Shawn Davidson, Chris White
# CSCI 404 - Fall 2018
# Assignment 2
       

def distance(target, source, insertcost, deletecost, replacecost,
             src_align, dashes, tgt_align):
    n = len(target)+1
    m = len(source)+1
    dist = [[0 for j in range(m)] for i in range(n)]
    for i in range(1,n):
        dist[i][0] = dist[i-1][0] + insertcost
    for j in range(1,m):
        dist[0][j] = dist[0][j-1] + deletecost
    for j in range(1,m):
        for i in range(1,n):
            inscost = insertcost  + dist[i-1][j]
            delcost = deletecost + dist[i][j-1]
            if(source[j-1] == target[i-1]): add = 0
            else: add = replacecost
            substcost = add + dist[i-1][j-1]
            dist[i][j] = min(inscost, delcost, substcost)
    
    i = n - 1
    j = m - 1
    s = j-1 # to keep track of position in source    
    t = i-1 # to leep track of position in target

    # Backtracing through the matrix to determine what edits are made
    while (i > 0 or j > 0):
        # Find the next location in the matrix
        if(i > 0 and j > 0):
            smallest = min(dist[i][j-1], dist[i-1][j-1], dist[i-1][j])
        elif(j == 0 and i > 0):
            smallest = dist[i-1][0]
        elif(i == 0 and j > 0):
            smallest = dist[0][j-1]
        else:
            smallest = dist[i][j]
        #substitution
        if (dist[i-1][j-1] == smallest or dist[i][j] == smallest):
            if(smallest == dist[i][j]):
                #make pipe
                dashes.append('|')                
            else:
                dashes.append(' ')
                #actual sub
            src_align.append(source[s])
            s = s-1
            tgt_align.append(target[t])
            t = t-1
            i = i-1
            j = j-1
        #deletion        
        elif (dist[i][j-1] == smallest):
            tgt_align.append('_')
            src_align.append(source[s])
            s = s-1
            dashes.append(' ')
            j = j-1
        #insertion
        else:
            src_align.append('_')
            tgt_align.append(target[t])
            t = t-1
            dashes.append(' ')
            i = i-1
            
    
    return dist[n-1][m-1]

if __name__=="__main__":
    from sys import argv
    if len(argv) > 2:
        src_align = []
        dashes = []
        tgt_align = []
        print("levenshtein distance =", distance(argv[1], argv[2], 1, 1, 2,
                                                 src_align, dashes, tgt_align))
        print(''.join(tgt_align[::-1]))
        print(''.join(dashes[::-1]))
        print(''.join(src_align[::-1]))

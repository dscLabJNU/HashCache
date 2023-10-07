import numpy as np
import traceback

# A Dynamic Programming solution for subset sum problem
# Returns true if there is a subset of set with sum equal to given sum

def isSubsetSum(S, n, M):
    # The value of subset[i, j] will be
    # true if there is a subset of
    # set[0..j-1] with sum equal to i
    subset = np.array([[True]*(M+1)]*(n+1))

    # If sum is 0, then answer is true
    for i in range(0, n+1):
        subset[i, 0] = True

    # If sum is not 0 and set is empty,
    # then answer is false
    for i in range(1, M+1):
        subset[0, i] = False

    # Fill the subset table in bottom-up manner
    for i in range(1, n+1):
        for j in range(1, M+1):
            if j < S[i-1]:
                subset[i, j] = subset[i-1, j]
            else:
                subset[i, j] = subset[i-1, j] or subset[i-1, j-S[i-1]]

    # print the True-False table
    # for i in range(0, n+1):
    #     for j in range(0, M+1):
    #         print('%-6s'%subset[i][j], end="  ")
    #     print(" ")

    if subset[n, M]:
        # print("Found a subset with given sum")
        sol = []
        # using backtracing to find the solution
        i = n
        while i >= 0:
            if subset[i, M] and not subset[i-1, M]:
                sol.append(S[i-1])
                M -= S[i-1]
            if M == 0:
                break
            i -= 1
        return sol
    else:
        return "No subset with given sum"

def main(args):
    try:
        len_seq = args.get('len_seq', 600)
        subset_sum = args.get("subset_sum", 1197)
        # test
        st = [i for i in range(len_seq)]
        n = len(st)
        res = isSubsetSum(st, n, subset_sum)
        return {"candidates": res}

    except Exception as e:
        return {"body": {"cust_error":traceback.format_exc()}}

def test():
    for subset_sum in [1674, 5174, 2222, 2268, 6197, 9527]:
        """
        sm values:
        1674
        5174
        2222
        2268
        6197
        9527
        """
        result = main({"subset_sum": subset_sum})
        print(result)
        print("SUM of the sequence:", sum(result['candidates']))

# test()
# print(main({}))
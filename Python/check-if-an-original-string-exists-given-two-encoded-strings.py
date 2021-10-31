# Time:  O(m * n * k), k is the max number of consecutive digits in s1 and s2
# Space: O(m * n * k)

# top-down dp (faster since accessing less states)
class Solution(object):
    def possiblyEquals(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: bool
        """
        def possible_numbers(s):  # Time: O(2^l), Space: O(2^l), l is the length of consecutive digits
            dp = [set() for _ in xrange(len(s))]
            for i in xrange(len(s)):
                curr, basis = 0, 1
                for j in reversed(xrange(i+1)):
                    curr += int(s[j])*basis
                    basis *= 10
                    if s[j] == '0':
                        continue
                    if j == 0:
                        dp[i].add(curr)
                    else:
                        dp[i].update(x+curr for x in dp[j-1])        
            return dp[-1]
    
        def memoization(s1, s2, i, j, k, lookup):
            if (i, j, k) not in lookup:
                if i == len(s1) and j == len(s2):
                    lookup[(i, j, k)] = (k == 0)
                elif i != len(s1) and s1[i].isdigit():
                    lookup[(i, j, k)] = False
                    for ni in xrange(i+1, len(s1)+1):
                        if ni == len(s1) or not s1[ni].isdigit():
                            break
                    for x in possible_numbers(s1[i:ni]):
                        if memoization(s1, s2, ni, j, k+x, lookup):
                            lookup[(i, j, k)] = True
                            break
                elif j != len(s2) and s2[j].isdigit():
                    lookup[(i, j, k)] = False
                    for nj in xrange(j+1, len(s2)+1):
                        if nj == len(s2) or not s2[nj].isdigit():
                            break
                    for x in possible_numbers(s2[j:nj]):
                        if memoization(s1, s2, i, nj, k-x, lookup):
                            lookup[(i, j, k)] = True
                            break
                elif k < 0:
                    lookup[(i, j, k)] = memoization(s1, s2, i+1, j, k+1, lookup) if i != len(s1) else False
                elif k > 0:
                    lookup[(i, j, k)] = memoization(s1, s2, i, j+1, k-1, lookup) if j != len(s2) else False
                else:
                    lookup[(i, j, k)] = memoization(s1, s2, i+1, j+1, 0, lookup) if i != len(s1) and j != len(s2) and s1[i] == s2[j] else False
            return lookup[(i, j, k)]

        return memoization(s1, s2, 0, 0, 0, {})


# Time:  O(m * n * k), k is the max number of consecutive digits in s1 and s2
# Space: O(m * n * k)
# top-down dp (faster since accessing less states)
class Solution2(object):
    def possiblyEquals(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: bool
        """
        def memoization(s1, s2, i, j, k, lookup):
            if (i, j, k) not in lookup:
                if i == len(s1) and j == len(s2):
                    lookup[(i, j, k)] = (k == 0)
                elif i != len(s1) and s1[i].isdigit():
                    lookup[(i, j, k)] = False
                    for ni in xrange(i+1, len(s1)+1):
                        if (ni == len(s1) or s1[ni] != '0') and memoization(s1, s2, ni, j, k+int(s1[i:ni]), lookup):
                            lookup[(i, j, k)] = True
                            break
                        if ni == len(s1) or not s1[ni].isdigit():
                            break
                elif j != len(s2) and s2[j].isdigit():
                    lookup[(i, j, k)] = False
                    for nj in xrange(j+1, len(s2)+1):
                        if (nj == len(s2) or s2[nj] != '0') and memoization(s1, s2, i, nj, k-int(s2[j:nj]), lookup):
                            lookup[(i, j, k)] = True
                            break
                        if nj == len(s2) or not s2[nj].isdigit():
                            break
                elif k < 0:
                    lookup[(i, j, k)] = memoization(s1, s2, i+1, j, k+1, lookup) if i != len(s1) else False
                elif k > 0:
                    lookup[(i, j, k)] = memoization(s1, s2, i, j+1, k-1, lookup) if j != len(s2) else False
                else:
                    lookup[(i, j, k)] = memoization(s1, s2, i+1, j+1, 0, lookup) if i != len(s1) and j != len(s2) and s1[i] == s2[j] else False
            return lookup[(i, j, k)]

        return memoization(s1, s2, 0, 0, 0, {})


# Time:  O(m * n * k), k is the max number of consecutive digits in s1 and s2
# Space: O(min(m, n) * k)
# bottom-up dp
class Solution3(object):
    def possiblyEquals(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: bool
        """
        MAX_DIGIT_LEN = 3
        w = 1+MAX_DIGIT_LEN
        dp = [[{} for _ in xrange(len(s2)+1)] for _ in xrange(w)]
        dp[0][0][0] = True
        for i in xrange(len(s1)+1):
            if i:
                dp[(i-1)%w] = [{} for _ in xrange(len(s2)+1)]
            for j in xrange(len(s2)+1):
                for k, v in dp[i%w][j].iteritems():
                    if not v:
                        continue
                    if i != len(s1) and j != len(s2) and s1[i] == s2[j] and k == 0:
                        dp[(i+1)%w][j+1][k] = True
                    if k <= 0 and i != len(s1):
                        if s1[i].isalpha():
                            if k:
                                dp[(i+1)%w][j][k+1] = True
                        elif s1[i] != '0':
                            curr = 0
                            for ni in xrange(i, len(s1)):
                                if not s1[ni].isdigit():
                                    break
                                curr = curr*10 + int(s1[ni])
                                dp[(ni+1)%w][j][k+curr] = True
                    if k >= 0 and j != len(s2):
                        if s2[j].isalpha():
                            if k:
                                dp[i%w][j+1][k-1] = True
                        elif s2[j] != '0':
                            curr = 0
                            for nj in xrange(j, len(s2)):
                                if not s2[nj].isdigit():
                                    break
                                curr = curr*10 + int(s2[nj])
                                dp[i%w][nj+1][k-curr] = True
        return 0 in dp[len(s1)%w][len(s2)] and dp[len(s1)%w][len(s2)][0]

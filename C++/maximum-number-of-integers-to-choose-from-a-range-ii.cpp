// Time:  O(blogb + logn * logb)
// Space: O(b)

// binary search, prefix sum
class Solution {
public:
    int maxCount(vector<int>& banned, int n, long long maxSum) {
        unordered_set<int> banned_set(cbegin(banned), cend(banned));
        vector<int> sorted_banned(cbegin(banned_set), cend(banned_set));
        sort(begin(sorted_banned), end(sorted_banned));
        vector<int64_t> prefix(size(sorted_banned) + 1);
        for (int i = 0; i < size(sorted_banned); ++i) {
            prefix[i + 1] = prefix[i] + sorted_banned[i];
        }
        const auto& check = [&](const int64_t x) {
            return (x + 1) * x / 2 - prefix[distance(cbegin(sorted_banned), upper_bound(cbegin(sorted_banned), cend(sorted_banned), x))] <= maxSum;
        };
        int left = 1, right = n;
        while (left <= right) {
            const auto mid = left + (right - left) / 2;
            if (!check(mid)) {
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        } 
        return right - distance(cbegin(sorted_banned), upper_bound(cbegin(sorted_banned), cend(sorted_banned), right));
    }
};

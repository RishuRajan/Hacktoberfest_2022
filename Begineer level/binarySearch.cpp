#include <bits/stdc++.h>
using namespace std;

int binarySearch(vector<int> v, int To_find)
{
    int lo = 0, hi = v.size() - 1;
    int mid; // this below check cover all the cases
    while (hi - lo > 1)
    {
        int mid = lo + (hi - lo) / 2;
        if (v[mid] < To_find)
        {
            lo = mid + 1;
        }
        else
        {
            hi = mid;
        }
    }
    if (v[lo] == To_find)
    {
        cout << "Found"
             << "At Index" << lo << endl;
    }
    else if (v[hi] == To_find)
    {
        cout << "Found"
             << "At inddex" << hi << endl;
    }
    else
    {
        cout << "Not Found" << endl;
    }
}

int main()
{
    vector<int> v = {1, 3, 5, 6};
    int To_find = 1;
    binarySearch(v, To_find);
    To_find = 6;
    binarySearch(v, To_find);
    To_find = 10;
    binarySearch(v, To_find);
    return 0;
}
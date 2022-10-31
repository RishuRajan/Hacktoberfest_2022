class Node{
    public:
    Node* v[26];
    Node(){
        for(int i=0;i<26;i++){
            v[i] = NULL;
        }
    }
};

class Trie{
private:
    Node* root;
public:
    Trie(){
        root = new Node();
    }
    void insert(string& s){
        Node* temp = root;
        for(int i=0;i<s.length();i++){
            if(temp->v[s[i]-'a']==NULL){
                Node* p = new Node();
                temp->v[s[i]-'a'] = p;
            }
            temp = temp->v[s[i]-'a'];
        }
    }
    void check(string& s, vector<vector<string>>& ans, vector<bool>& isFilled){
        Node* temp = root;
        for(int i=0;i<s.length();i++){
            if(temp->v[s[i]-'a']==NULL) break;
            temp = temp->v[s[i]-'a'];
            isFilled[i] = true;
            ans[i].push_back(s);
        }
    }
};


class Solution{
public:
    vector<vector<string>> displayContacts(int n, string contact[], string s)
    {
        // code here
        Trie t;
        t.insert(s);
        sort(contact,contact+n);
        int len = s.length();
        vector<vector<string>> ans(len,vector<string>());
        vector<bool> isFilled(len,false);
        for(int i=0;i<n;i++){
            if(i>0 && contact[i]==contact[i-1]) continue;
            t.check(contact[i],ans,isFilled);
        }
        for(int i=0;i<len;i++){
            if(!isFilled[i]){
                ans[i] = {"0"};
            }
        }
        return ans;
    }
};
 

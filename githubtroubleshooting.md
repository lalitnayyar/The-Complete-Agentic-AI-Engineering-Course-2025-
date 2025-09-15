# GitHub Troubleshooting Guide

## 🔐 Authentication Issues

### Problem: "Invalid username or token. Password authentication is not supported"

**Error Message:**
```
Username for 'https://github.com': lalitnayyar@gmail.com
Password for 'https://lalitnayyar%40gmail.com@github.com':
remote: Invalid username or token. Password authentication is not supported for Git operations.
fatal: Authentication failed for 'https://github.com/lalitnayyar/The-Complete-Agentic-AI-Engineering-Course-2025-.git/'
```

**Root Cause:** GitHub deprecated password authentication for Git operations on August 13, 2021. You must now use either:
- Personal Access Token (PAT)
- SSH Key authentication

---

## 🛠️ Solutions

### Solution 1: Personal Access Token (PAT) - Quick Fix

#### Step 1: Create a Personal Access Token
1. Go to [GitHub.com](https://github.com) → Settings
2. Navigate to **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. Click **"Generate new token (classic)"**
4. Fill in the form:
   - **Note**: "Agentic AI Course Development"
   - **Expiration**: Choose appropriate duration (30 days, 90 days, or No expiration)
   - **Scopes**: Select `repo` (Full control of private repositories)
5. Click **"Generate token"**
6. **Copy the token immediately** (you won't see it again!)

#### Step 2: Use the Token
```bash
git push origin main
# When prompted:
# Username: lalitnayyar@gmail.com
# Password: [paste your token here, not your GitHub password]
```

#### Step 3: Store Credentials (Optional)
```bash
git config --global credential.helper store
# This will save your credentials for future use
```

---

### Solution 2: SSH Key Authentication - Long-term Solution

#### Step 1: Generate SSH Key
```bash
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/id_ed25519 -N ""
```

#### Step 2: Add SSH Key to GitHub
1. **Display your public key:**
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. **Copy the output** (starts with `ssh-ed25519`)

3. **Add to GitHub:**
   - Go to GitHub.com → Settings → SSH and GPG keys
   - Click **"New SSH key"**
   - **Title**: "WSL2 Development Machine" (or your preferred name)
   - **Key**: Paste the public key
   - Click **"Add SSH key"**

#### Step 3: Test SSH Connection
```bash
ssh -T git@github.com
# Should return: "Hi username! You've successfully authenticated..."
```

#### Step 4: Switch Remote URL to SSH
```bash
git remote set-url origin git@github.com:username/repository-name.git
```

#### Step 5: Push with SSH
```bash
git push origin main
```

---

## 🔄 Switching Between HTTPS and SSH

### Check Current Remote URL
```bash
git remote -v
```

### Switch to SSH
```bash
git remote set-url origin git@github.com:username/repository-name.git
```

### Switch to HTTPS
```bash
git remote set-url origin https://github.com/username/repository-name.git
```

---

## 🚨 Common Issues and Fixes

### Issue 1: "Permission denied (publickey)"
**Cause:** SSH key not added to GitHub or wrong key being used

**Fix:**
1. Verify SSH key is added to GitHub
2. Test connection: `ssh -T git@github.com`
3. Check if using correct key: `ssh-add -l`

### Issue 2: "Authentication failed" with PAT
**Cause:** Wrong token or expired token

**Fix:**
1. Generate new token with correct permissions
2. Ensure `repo` scope is selected
3. Use token as password, not GitHub password

### Issue 3: "Repository not found"
**Cause:** Wrong repository URL or insufficient permissions

**Fix:**
1. Verify repository URL is correct
2. Check if repository exists and you have access
3. Ensure token has `repo` scope

### Issue 4: "Push rejected" - Branch protection
**Cause:** Branch has protection rules

**Fix:**
1. Check branch protection settings
2. Use pull request workflow
3. Contact repository administrator

---

## 📋 Step-by-Step Troubleshooting Checklist

### For HTTPS Authentication:
- [ ] Created Personal Access Token
- [ ] Selected `repo` scope
- [ ] Copied token before closing GitHub page
- [ ] Using token as password (not GitHub password)
- [ ] Repository URL is correct

### For SSH Authentication:
- [ ] Generated SSH key pair
- [ ] Added public key to GitHub account
- [ ] Tested SSH connection successfully
- [ ] Switched remote URL to SSH format
- [ ] Private key is in correct location (`~/.ssh/`)

### General Checks:
- [ ] Git is configured with correct user name and email
- [ ] Repository exists and is accessible
- [ ] Local changes are committed
- [ ] Branch exists on remote
- [ ] No merge conflicts

---

## 🔧 Advanced Troubleshooting

### Clear Stored Credentials
```bash
# Clear stored credentials
git config --global --unset credential.helper
# Or remove from credential store
rm ~/.git-credentials
```

### Debug SSH Connection
```bash
# Verbose SSH connection test
ssh -vT git@github.com
```

### Check Git Configuration
```bash
# View all Git configuration
git config --list --global
```

### Reset Remote URL
```bash
# Remove and re-add remote
git remote remove origin
git remote add origin git@github.com:username/repository-name.git
```

---

## 📚 Additional Resources

- [GitHub Personal Access Tokens Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub SSH Key Documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [Git Credential Storage](https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage)

---

## 🎯 Quick Reference Commands

```bash
# Check remote URL
git remote -v

# Switch to SSH
git remote set-url origin git@github.com:username/repo.git

# Switch to HTTPS
git remote set-url origin https://github.com/username/repo.git

# Test SSH connection
ssh -T git@github.com

# Configure credential storage
git config --global credential.helper store

# View Git configuration
git config --list --global
```

---

*This guide covers the most common GitHub authentication issues encountered when pushing code to repositories. For additional help, refer to GitHub's official documentation or contact support.*

# 📤 Đẩy code lên GitHub

## ✅ Đã hoàn tất:
- ✅ Git init
- ✅ Git add .
- ✅ Git commit

## 🚀 Các bước tiếp theo:

### Bước 1: Tạo repository trên GitHub

1. Mở: https://github.com/new
2. Đặt tên repository: **`fullstack-react-fastapi`** (hoặc tên khác)
3. **KHÔNG** tích vào: Add README, .gitignore, license
4. Click **"Create repository"**

### Bước 2: Push code lên GitHub

GitHub sẽ hiển thị commands, nhưng bạn chỉ cần chạy:

```bash
# Thay YOUR_USERNAME và YOUR_REPO bằng thông tin của bạn
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

**Ví dụ:**
```bash
git remote add origin https://github.com/johndoe/fullstack-react-fastapi.git
git branch -M main
git push -u origin main
```

### Bước 3: Nhập thông tin đăng nhập

Khi push, Git sẽ yêu cầu:
- **Username**: GitHub username của bạn
- **Password**: Dùng **Personal Access Token** (KHÔNG phải password)

#### Tạo Personal Access Token:
1. Mở: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Đặt tên: **"Git Push Token"**
4. Tích: ☑️ **repo** (full control)
5. Click **"Generate token"**
6. **Sao chép token** (chỉ hiện 1 lần!)
7. Dùng token này làm password khi push

---

## 🔧 Commands đầy đủ:

```bash
# Kiểm tra status
git status

# Kiểm tra remote
git remote -v

# Đổi tên branch sang main
git branch -M main

# Thêm remote (thay YOUR_USERNAME/YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push lên GitHub
git push -u origin main
```

---

## 📝 Lần push tiếp theo:

Sau khi setup xong, những lần sau chỉ cần:

```bash
git add .
git commit -m "Your commit message"
git push
```

---

## 🎯 File script đã tạo sẵn:

**File: `git-push.bat`** - Click đúp để push (sau khi setup remote)

---

## ❓ Khắc phục lỗi:

### Lỗi: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

### Lỗi: "Authentication failed"
- Đảm bảo dùng **Personal Access Token** thay vì password
- Token phải có quyền **repo**

### Lỗi: "failed to push some refs"
```bash
git pull origin main --rebase
git push -u origin main
```

---

## 🌟 Sau khi push thành công:

Repository của bạn sẽ có tại:
```
https://github.com/YOUR_USERNAME/YOUR_REPO
```

Chia sẻ link này với mọi người! 🎉

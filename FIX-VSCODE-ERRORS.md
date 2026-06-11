# 🔧 Sửa lỗi "code đỏ" trong VS Code

## Lỗi 1: "Unknown at rule @tailwind" ⚠️

### Nguyên nhân:
VS Code CSS validator không nhận diện Tailwind CSS directives (@tailwind, @apply, @layer)

### ✅ Cách sửa:

**Cách 1: Cài Tailwind CSS IntelliSense Extension (Khuyến nghị)** ⭐⭐⭐
1. Mở VS Code Extensions: **Ctrl + Shift + X**
2. Tìm: **"Tailwind CSS IntelliSense"**
3. Click **Install** (tác giả: Tailwind Labs)
4. Reload VS Code

**Cách 2: Tắt CSS validation (Nhanh)**
1. Mở Command Palette: **Ctrl + Shift + P**
2. Gõ: **"Preferences: Open Settings (JSON)"**
3. Thêm vào:
```json
{
  "css.validate": false,
  "files.associations": {
    "*.css": "tailwindcss"
  }
}
```

Đã tạo sẵn file `.vscode/settings.json` - chỉ cần **Reload Window**!

---

## Lỗi 2: Code TypeScript đỏ lòm 🔴

### Nguyên nhân:
- VS Code chưa nhận diện TypeScript workspace
- Path aliases (@/*) chưa được nhận diện
- TypeScript server cần reload

### ✅ Cách sửa nhanh:

**Bước 1: Reload VS Code TypeScript Server**
1. Mở Command Palette: **Ctrl + Shift + P**
2. Gõ: **"TypeScript: Restart TS Server"**
3. Enter

**Bước 2: Reload Window**
1. Mở Command Palette: **Ctrl + Shift + P**
2. Gõ: **"Developer: Reload Window"**
3. Enter

**Bước 3: Chọn TypeScript workspace**
1. Mở bất kỳ file `.tsx` nào
2. Nhìn xuống góc dưới bên phải status bar
3. Click vào version TypeScript (ví dụ: "TypeScript 5.3.3")
4. Chọn: **"Use Workspace Version"**

---

## 🔍 Nếu vẫn lỗi:

### Kiểm tra 1: Node modules đã cài chưa?
```bash
cd frontend
npm install
```

### Kiểm tra 2: TypeScript config đúng chưa?
File `frontend/tsconfig.json` phải có:
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### Kiểm tra 3: VS Code settings
File `.vscode/settings.json` đã được tạo tự động!

---

## 🎯 Các lỗi thường gặp:

### Lỗi: Cannot find module '@/...'
**Giải pháp:** 
- Restart TS Server (Ctrl+Shift+P → TypeScript: Restart TS Server)
- Đảm bảo đang ở workspace `frontend` folder

### Lỗi: Cannot find module 'zustand'
**Giải pháp:**
```bash
cd frontend
npm install zustand
```

### Lỗi: Cannot find module 'path'
**Giải pháp:**
```bash
cd frontend
npm install --save-dev @types/node
```

### Lỗi: Unknown at rule @tailwind
**Giải pháp:**
- Cài extension: Tailwind CSS IntelliSense
- Hoặc settings đã tắt validation tự động

---

## 🚀 Script tự động sửa:

File `fix-frontend.bat` đã được tạo, click đúp để chạy!

---

## 💡 Lưu ý:

- Lỗi đỏ trong editor KHÔNG ảnh hưởng đến việc chạy app
- App vẫn build và chạy bình thường với Docker
- Đây chỉ là lỗi hiển thị của VS Code IntelliSense

---

## ✨ Extensions khuyến nghị:

Khi mở VS Code, nó sẽ đề xuất cài các extensions sau:
1. **Tailwind CSS IntelliSense** - Autocomplete Tailwind classes
2. **ESLint** - Linting JavaScript/TypeScript
3. **Prettier** - Code formatter

---

## ✅ Sau khi sửa:

1. Mở file `frontend/src/App.tsx`
2. Nếu không còn lỗi đỏ → Thành công! ✅
3. File `index.css` không còn warning @tailwind → Thành công! ✅
4. Nếu vẫn đỏ → Thử restart VS Code hoàn toàn (tắt và mở lại)

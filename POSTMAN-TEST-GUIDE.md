# 📮 POSTMAN TEST GUIDE - Chi Tiết Các Trường Cần Nhập

## 🔧 Setup Postman

### 1. Set Base URL
Trong Postman, tạo **Environment Variable**:
```
API_URL = http://localhost:8000
Token = (sẽ lấy sau khi login)
```

### 2. Base URL Setup
Tất cả requests sử dụng:
```
{{API_URL}}/api/v1
```

---

## 🔐 AUTHENTICATION (Auth Endpoints)

### 1️⃣ REGISTER - Tạo tài khoản mới

**Endpoint:**
```
POST {{API_URL}}/api/v1/auth/register
```

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "email": "user1@example.com",
  "password": "password123",
  "username": "john_doe"
}
```

**Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "260101000001",
    "account_id": 1,
    "username": "john_doe",
    "created_at": "2026-06-30T12:00:00+00:00",
    "updated_at": null
  }
}
```

**Errors:**
- ❌ `400` - Email already registered
- ❌ `400` - Username already taken
- ❌ `422` - Invalid email format

**Test Data:**
```
✅ user1@example.com / pass123 / john_doe
✅ user2@example.com / pass456 / jane_doe
✅ user3@example.com / pass789 / alice_smith
```

---

### 2️⃣ LOGIN - Đăng nhập

**Endpoint:**
```
POST {{API_URL}}/api/v1/auth/login
```

**Headers:**
```
Content-Type: application/x-www-form-urlencoded
```

**Body (Form Data):**
```
username: user1@example.com
password: password123
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "260101000001",
    "account_id": 1,
    "username": "john_doe",
    "created_at": "2026-06-30T12:00:00+00:00",
    "updated_at": null
  }
}
```

**Errors:**
- ❌ `401` - Incorrect email or password
- ❌ `400` - Account is inactive

**💾 Save Token:**
Sau khi login, copy `access_token` vào Postman Environment:
```
Token = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Hoặc auto-save bằng Script:
```javascript
var jsonData = pm.response.json();
pm.environment.set("Token", jsonData.access_token);
```

---

## 👥 USERS (User Endpoints)

### 1️⃣ GET ALL USERS - Lấy danh sách users

**Endpoint:**
```
GET {{API_URL}}/api/v1/users/?skip=0&limit=100
```

**Headers:**
```
Content-Type: application/json
```

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| skip | int | 0 | Số bản ghi bỏ qua |
| limit | int | 100 | Số bản ghi trả về |

**Response (200 OK):**
```json
[
  {
    "id": "260101000001",
    "account_id": 1,
    "username": "john_doe",
    "created_at": "2026-06-30T12:00:00+00:00",
    "updated_at": null
  },
  {
    "id": "260101000002",
    "account_id": 2,
    "username": "jane_doe",
    "created_at": "2026-06-30T12:05:00+00:00",
    "updated_at": null
  }
]
```

---

### 2️⃣ GET CURRENT USER - Lấy thông tin user đang đăng nhập

**Endpoint:**
```
GET {{API_URL}}/api/v1/users/me
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {{Token}}
```

⚠️ **REQUIRE JWT TOKEN** - Phải có token từ login

**Response (200 OK):**
```json
{
  "id": "260101000001",
  "account_id": 1,
  "username": "john_doe",
  "created_at": "2026-06-30T12:00:00+00:00",
  "updated_at": null
}
```

**Errors:**
- ❌ `401` - Not authenticated (token missing)
- ❌ `401` - Token expired
- ❌ `401` - Invalid token

---

### 3️⃣ GET USER BY ID - Lấy thông tin user theo ID

**Endpoint:**
```
GET {{API_URL}}/api/v1/users/{user_id}
```

**Parameters:**
| Param | Type | Required | Example |
|-------|------|----------|---------|
| user_id | string | ✅ | `260101000001` |

**Response (200 OK):**
```json
{
  "id": "260101000001",
  "account_id": 1,
  "username": "john_doe",
  "created_at": "2026-06-30T12:00:00+00:00",
  "updated_at": null
}
```

**Errors:**
- ❌ `404` - User not found

---

## 📝 POSTS (Post Endpoints)

### 1️⃣ CREATE POST - Tạo bài viết

**Endpoint:**
```
POST {{API_URL}}/api/v1/posts/
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {{Token}}
```

⚠️ **REQUIRE JWT TOKEN**

**Body (JSON):**
```json
{
  "title": "My First Post",
  "content": "This is my first post on the platform. It's awesome!"
}
```

**Field Requirements:**
| Field | Type | Required | Min | Max | Notes |
|-------|------|----------|-----|-----|-------|
| title | string | ✅ | 1 | 255 | Required, non-empty |
| content | string | ✅ | 1 | - | Required, non-empty |

**Response (201 Created):**
```json
{
  "id": 1,
  "user_id": "260101000001",
  "title": "My First Post",
  "content": "This is my first post on the platform. It's awesome!",
  "created_at": "2026-06-30T12:30:00+00:00",
  "updated_at": null
}
```

**Errors:**
- ❌ `401` - Not authenticated
- ❌ `422` - Validation error (empty title/content)

**Test Data:**
```json
✅ {"title": "Hello World", "content": "First post!"}
✅ {"title": "Testing API", "content": "Testing the API endpoints..."}
✅ {"title": "Great Day", "content": "It's a beautiful day today!"}
```

---

### 2️⃣ GET ALL POSTS - Lấy danh sách posts

**Endpoint:**
```
GET {{API_URL}}/api/v1/posts/?skip=0&limit=100
```

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| skip | int | 0 | Số bài viết bỏ qua |
| limit | int | 100 | Số bài viết trả về |

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "user_id": "260101000001",
    "title": "My First Post",
    "content": "This is my first post on the platform. It's awesome!",
    "created_at": "2026-06-30T12:30:00+00:00",
    "updated_at": null
  },
  {
    "id": 2,
    "user_id": "260101000002",
    "title": "Hello Everyone",
    "content": "Excited to be here!",
    "created_at": "2026-06-30T12:35:00+00:00",
    "updated_at": null
  }
]
```

---

### 3️⃣ GET POST BY ID - Lấy chi tiết post

**Endpoint:**
```
GET {{API_URL}}/api/v1/posts/{post_id}
```

**Parameters:**
| Param | Type | Required | Example |
|-------|------|----------|---------|
| post_id | integer | ✅ | `1` |

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "260101000001",
  "title": "My First Post",
  "content": "This is my first post on the platform. It's awesome!",
  "created_at": "2026-06-30T12:30:00+00:00",
  "updated_at": null
}
```

**Errors:**
- ❌ `404` - Post not found

---

### 4️⃣ UPDATE POST - Cập nhật bài viết

**Endpoint:**
```
PUT {{API_URL}}/api/v1/posts/{post_id}
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {{Token}}
```

**Parameters:**
| Param | Type | Required | Example |
|-------|------|----------|---------|
| post_id | integer | ✅ | `1` |

**Body (JSON):**
```json
{
  "title": "Updated Title",
  "content": "Updated content here"
}
```

**Field Requirements:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| title | string | ❌ | Optional, nếu có sẽ update |
| content | string | ❌ | Optional, nếu có sẽ update |

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "260101000001",
  "title": "Updated Title",
  "content": "Updated content here",
  "created_at": "2026-06-30T12:30:00+00:00",
  "updated_at": "2026-06-30T12:45:00+00:00"
}
```

**Errors:**
- ❌ `401` - Not authenticated
- ❌ `403` - Not authorized (bạn không phải là tác giả)
- ❌ `404` - Post not found

**Test Cases:**
```json
✅ {"title": "New Title"}                    # Chỉ update title
✅ {"content": "New content"}                # Chỉ update content
✅ {"title": "Both", "content": "Updated"}   # Update cả hai
```

---

### 5️⃣ DELETE POST - Xóa bài viết

**Endpoint:**
```
DELETE {{API_URL}}/api/v1/posts/{post_id}
```

**Headers:**
```
Authorization: Bearer {{Token}}
```

**Parameters:**
| Param | Type | Required | Example |
|-------|------|----------|---------|
| post_id | integer | ✅ | `1` |

**Response (204 No Content):**
```
(empty body)
```

**Errors:**
- ❌ `401` - Not authenticated
- ❌ `403` - Not authorized
- ❌ `404` - Post not found

---

## ❤️ FOLLOWS (Follow Endpoints)

### 1️⃣ FOLLOW USER - Theo dõi người dùng

**Endpoint:**
```
POST {{API_URL}}/api/v1/follows/?follower_id={{USER_ID}}
```

**Headers:**
```
Content-Type: application/json
```

**Query Parameters:**
| Param | Type | Required | Example | Notes |
|-------|------|----------|---------|-------|
| follower_id | string | ✅ | `260101000001` | User ID của người theo dõi |

**Body (JSON):**
```json
{
  "following_id": "260101000002"
}
```

**Field Requirements:**
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| following_id | string | ✅ | User ID của người bị theo dõi |

**Response (201 Created):**
```json
{
  "id": 1,
  "follower_id": "260101000001",
  "following_id": "260101000002",
  "created_at": "2026-06-30T12:50:00+00:00"
}
```

**Errors:**
- ❌ `404` - User not found
- ❌ `400` - Cannot follow yourself
- ❌ `400` - Already following

**Test Data:**
```
follower_id=260101000001&following_id=260101000002
follower_id=260101000001&following_id=260101000003
follower_id=260101000002&following_id=260101000001
```

---

### 2️⃣ GET FOLLOWERS - Lấy danh sách followers

**Endpoint:**
```
GET {{API_URL}}/api/v1/follows/followers/{user_id}
```

**Parameters:**
| Param | Type | Required | Example |
|-------|------|----------|---------|
| user_id | string | ✅ | `260101000001` |

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "follower_id": "260101000002",
    "following_id": "260101000001",
    "created_at": "2026-06-30T12:50:00+00:00"
  },
  {
    "id": 2,
    "follower_id": "260101000003",
    "following_id": "260101000001",
    "created_at": "2026-06-30T12:55:00+00:00"
  }
]
```

---

### 3️⃣ GET FOLLOWING - Lấy danh sách đang theo dõi

**Endpoint:**
```
GET {{API_URL}}/api/v1/follows/following/{user_id}
```

**Parameters:**
| Param | Type | Required | Example |
|-------|------|----------|---------|
| user_id | string | ✅ | `260101000001` |

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "follower_id": "260101000001",
    "following_id": "260101000002",
    "created_at": "2026-06-30T12:50:00+00:00"
  }
]
```

---

### 4️⃣ UNFOLLOW - Bỏ theo dõi

**Endpoint:**
```
DELETE {{API_URL}}/api/v1/follows/{follow_id}
```

**Parameters:**
| Param | Type | Required | Example |
|-------|------|----------|---------|
| follow_id | string | ✅ | `1` |

**Response (204 No Content):**
```
(empty body)
```

**Errors:**
- ❌ `404` - Follow not found

---

## 🤝 FRIENDSHIPS (Friend Request Endpoints)

### 1️⃣ SEND FRIEND REQUEST - Gửi lời mời kết bạn

**Endpoint:**
```
POST {{API_URL}}/api/v1/friendships/{recipient_id}
```

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {{Token}}
```

**Parameters:**
| Param | Type | Required | Example | Notes |
|-------|------|----------|---------|-------|
| recipient_id | string | ✅ | `260101000002` | User ID người nhận |

**Body:**
```
(empty - no request body)
```

**Response (201 Created):**
```json
{
  "id": 1,
  "low_user": "260101000001",
  "high_user": "260101000002",
  "request_by": "260101000001",
  "status": "pending",
  "created_at": "2026-06-30T13:00:00+00:00",
  "updated_at": null
}
```

**Errors:**
- ❌ `401` - Not authenticated
- ❌ `404` - User not found
- ❌ `400` - Cannot add yourself as friend
- ❌ `400` - Friendship request already exists

---

### 2️⃣ GET FRIENDSHIPS - Lấy danh sách kết bạn

**Endpoint:**
```
GET {{API_URL}}/api/v1/friendships/
```

**Headers:**
```
Authorization: Bearer {{Token}}
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "low_user": "260101000001",
    "high_user": "260101000002",
    "request_by": "260101000001",
    "status": "pending",
    "created_at": "2026-06-30T13:00:00+00:00",
    "updated_at": null
  },
  {
    "id": 2,
    "low_user": "260101000001",
    "high_user": "260101000003",
    "request_by": "260101000001",
    "status": "accepted",
    "created_at": "2026-06-30T13:05:00+00:00",
    "updated_at": "2026-06-30T13:10:00+00:00"
  }
]
```

---

### 3️⃣ UPDATE FRIENDSHIP STATUS - Chấp nhận/Từ chối lời mời

**Endpoint:**
```
PUT {{API_URL}}/api/v1/friendships/{friendship_id}?status_str=accepted
```

**Headers:**
```
Authorization: Bearer {{Token}}
```

**Parameters:**
| Param | Type | Required | Example | Allowed Values |
|-------|------|----------|---------|-----------------|
| friendship_id | integer | ✅ | `1` | - |
| status_str | string | ✅ | `accepted` | `accepted`, `rejected` |

**Response (200 OK):**
```json
{
  "id": 1,
  "low_user": "260101000001",
  "high_user": "260101000002",
  "request_by": "260101000001",
  "status": "accepted",
  "created_at": "2026-06-30T13:00:00+00:00",
  "updated_at": "2026-06-30T13:15:00+00:00"
}
```

**Errors:**
- ❌ `401` - Not authenticated
- ❌ `403` - Only recipient can respond (bạn không phải người nhận)
- ❌ `404` - Friendship not found

**Test Cases:**
```
status_str=accepted   # Chấp nhận lời mời
status_str=rejected   # Từ chối lời mời
```

---

### 4️⃣ REMOVE FRIEND - Xóa bạn

**Endpoint:**
```
DELETE {{API_URL}}/api/v1/friendships/{friendship_id}
```

**Headers:**
```
Authorization: Bearer {{Token}}
```

**Parameters:**
| Param | Type | Required | Example |
|-------|------|----------|---------|
| friendship_id | integer | ✅ | `1` |

**Response (204 No Content):**
```
(empty body)
```

**Errors:**
- ❌ `401` - Not authenticated
- ❌ `403` - Not authorized
- ❌ `404` - Friendship not found

---

## 🧪 TEST SCENARIOS - Các Kịch Bản Test

### Scenario 1: Đầu Tiên
```
1. POST /auth/register
   Đăng ký user1: user1@example.com / pass123 / john_doe
   ✅ Copy token → Set {{Token}}

2. POST /auth/register
   Đăng ký user2: user2@example.com / pass456 / jane_doe
   ✅ Copy token2

3. POST /auth/login
   Login user1
   ✅ Verify token
```

### Scenario 2: Posts
```
1. POST /posts/
   User1 tạo post
   ✅ Nhận được post_id = 1

2. GET /posts/
   Xem tất cả posts
   ✅ Thấy post vừa tạo

3. PUT /posts/1
   User1 update post
   ✅ Status = 200

4. DELETE /posts/1
   User1 xóa post
   ✅ Status = 204
```

### Scenario 3: Follows
```
1. POST /follows/?follower_id=USER1_ID
   User1 follow user2
   ✅ Nhận follow_id

2. GET /follows/following/USER1_ID
   Xem user1 đang follow ai
   ✅ Thấy user2

3. DELETE /follows/{follow_id}
   Bỏ follow
   ✅ Status = 204
```

### Scenario 4: Friendships
```
1. POST /friendships/USER2_ID
   User1 gửi lời mời kết bạn cho user2
   ✅ status = "pending"

2. GET /friendships/
   (Đăng nhập với token của user1)
   ✅ Thấy friendship pending

3. PUT /friendships/1?status_str=accepted
   (Đăng nhập với token của user2)
   ✅ status = "accepted"

4. DELETE /friendships/1
   Xóa bạn
   ✅ Status = 204
```

---

## 🔒 AUTHORIZATION HEADERS

### Các Endpoint Cần Token:
- ✅ `POST /auth/login` (form-data)
- ✅ `GET /users/me`
- ✅ `POST /posts/`
- ✅ `PUT /posts/{id}`
- ✅ `DELETE /posts/{id}`
- ✅ `GET /friendships/`
- ✅ `POST /friendships/{id}`
- ✅ `PUT /friendships/{id}`
- ✅ `DELETE /friendships/{id}`

### Cách Set Token trong Postman:
1. **Tab Headers**
   ```
   Authorization: Bearer {{Token}}
   ```

2. **Hoặc Tab Authorization**
   - Type: Bearer Token
   - Token: `{{Token}}`

---

## ⚠️ COMMON ERRORS & SOLUTIONS

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Token missing/expired | Đăng nhập lại, copy token |
| 403 Forbidden | Không phải owner | Dùng account của chính người tạo |
| 404 Not Found | Resource không tồn tại | Kiểm tra ID |
| 422 Validation Error | Thiếu field hoặc format sai | Kiểm tra request body |
| 400 Bad Request | Logic validation fail | Kiểm tra các constraint (follow yourself, duplicate) |

---

## 📊 POSTMAN COLLECTION TEMPLATE

```json
{
  "info": {
    "name": "TDL API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "Register",
          "request": {
            "method": "POST",
            "url": "{{API_URL}}/api/v1/auth/register",
            "body": {
              "mode": "raw",
              "raw": "{\"email\":\"user1@example.com\",\"password\":\"pass123\",\"username\":\"john_doe\"}"
            }
          }
        },
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "url": "{{API_URL}}/api/v1/auth/login",
            "body": {
              "mode": "urlencoded",
              "urlencoded": [
                {"key":"username","value":"user1@example.com"},
                {"key":"password","value":"pass123"}
              ]
            }
          }
        }
      ]
    }
  ]
}
```

---

**Last Updated**: June 2026
**API Version**: v1
**Status**: 🟢 Ready for Testing

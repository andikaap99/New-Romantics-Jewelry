### 1. Authentication
#### Login (Dapatkan Token)
Endpoint ini digunakan untuk menukar username & password dengan access_token. Token ini wajib digunakan untuk mengakses fitur Transaksi.
- URL: /login
- Method: POST
- Format Body: application/x-www-form-urlencoded (BUKAN JSON!)

**Request Body**
| Key      | Tipe   | Wajib? | Keterangan                       |
|----------|--------|--------|----------------------------------|
| username | String | Ya     | Username user (contoh: andika99) |
| password | String | Ya     | Password user                    |

**Contoh Request (Javascript/Axios)**
```
const formData = new URLSearchParams();
formData.append('username', 'andika99');
formData.append('password', 'primer33');

axios.post('/login', formData, {
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
});
```

**Response Sukses (200 OK)**
```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Users
#### Register User Baru
Membuat user baru (Admin/Kasir).
- URL: /users
- Method: POST
- Format Body: application/json

**Request Body (JSON)**
| Key       | Tipe   | Wajib? | Keterangan                  |
|-----------|--------|--------|-----------------------------|
| nama_user | String | Ya     | Nama lengkap                |
| username  | String | Ya     | Username unik (untuk login) |
| password  | String | Ya     | Password                    |
| role      | String | Ya     | Contoh: admin, kasir        |

**Contoh Request**
```
{
  "nama_user": "Budi Santoso",
  "username": "budi123",
  "password": "rahasia123",
  "role": "kasir"
}
```

**Response Sukses (200 OK)**
```
{
  "nama_user": "Budi Santoso",
  "username": "budi123",
  "role": "kasir",
  "id_user": 2
}
```

### 3. Kategori & Produk
#### Tambah Kategori
- URL: /categories
- Method: POST
- Auth: Tidak Butuh (Optional, cuma kayanya harus login ga sih?)

**Request Body**
```
{
  "kode_kategori": "CINCIN-EMAS",
  "nama_kategori": "Cincin Emas Murni"
}
```

#### Lihat Semua Kategori
- URL: /categories
- Method: GET

#### Update Kategori (NEW UPDATE)
- URL: /categories/{kode_kategori}
- Method: PUT
- Contoh URL: /categories/DM-RING (Kode Lama)

**Request Body (JSON)**
```
{
  "kode_kategori": "DM-RING-NEW",
  "nama_kategori": "Cincin Berlian Mewah"
}
```

#### Delete Kategori (NEW UPDATE)
Menghapus kategori. PENTING: Kategori tidak bisa dihapus jika masih ada produk yang menggunakan kategori tersebut (Error 400).
- URL: /categories/{kode_kategori}
- Method: DELETE

**Response Sukses (200 OK)
```
{
  "message": "Kategori berhasil dihapus"
}
```

#### Tambah Produk
Pastikan kode_kategori sudah dibuat sebelumnya.
- URL: /products
- Method: POST

**Request Body**
```
{
  "nama_produk": "Cincin 24 Karat",
  "harga": 5000000,
  "stok": 10,
  "kode_kategori": "CINCIN-EMAS"
}
```

#### Lihat Semua Produk
- URL: /products
- Method: GET

**Response Sukses**
```
[
  {
    "nama_produk": "Cincin 24 Karat",
    "harga": 5000000,
    "stok": 10,
    "kode_kategori": "CINCIN-EMAS",
    "id_produk": 1
  }
]
```

#### Update Produk (NEW UPDATE)
Mengubah data produk (Harga, Nama, Stok) berdasarkan ID.
- URL: /products/{product_id}
- Method: PUT
- Contoh URL: /products/1

**Request Body (JSON)**
```
{
  "nama_produk": "Cincin Emas 24K (Revisi)",
  "harga": 5500000,
  "stok": 8,
  "kode_kategori": "DM-RING"
}
```

**Response Sukses (200 OK)**
Mengembalikan data produk yang sudah diperbarui.

#### Delete Produk (NEW UPDATE)
Menghapus produk dari database secara permanen.
- URL: /products/{product_id}
- Method: DELETE
- Contoh URL: /products/1

**Response Sukses (200 OK)**
```
{
  "message": "Produk berhasil dihapus"
}
```

### 4. Transaksi
#### Buat Transaksi Penjualan
Endpoint ini TERKUNCI (Protected). Wajib menyertakan Header Authorization dari hasil login. Stok produk akan berkurang otomatis.
- URL: /transactions
- Method: POST
- Headers: 
  - Authorization: Bearer <access_token_anda>
  - Content-Type: application/json

**Request Body (JSON)**
```
{
  "nama_pembeli": "Sultan Andara",
  "no_hp_pembeli": "08123456789",
  "kode_penjualan": "TRX-2025-001",
  "detail_produk": [
    {
      "id_produk": 1,
      "jumlah": 2
    },
    {
      "id_produk": 5,
      "jumlah": 1
    }
  ]
}
```

**Response Sukses (200 OK)**
```
{
  "nama_pembeli": "Sultan Andara",
  "no_hp_pembeli": "08123456789",
  "kode_penjualan": "TRX-2025-001",
  "tgl_transaksi": "2025-01-02T10:00:00",
  "detail_produk": [
    {
      "id_produk": 1,
      "jumlah": 2
    },
    {
      "id_produk": 5,
      "jumlah": 1
    }
  ]
}
```

Kemungkinan Error:
- 401 Unauthorized: Lupa pasang Header Token atau Token expired.
- 404 Not Found: ID Produk salah/tidak ada.
- 400 Bad Request: Stok produk tidak cukup.

#### Lihat Semua Riwayat Transaksi (NEW UPDATE)
Endpoint ini digunakan untuk halaman "Laporan Penjualan". Data ditampilkan lengkap dengan nama barang yang terjual.
- URL: /transactions
- Method: GET
- Auth: Wajib Login (Butuh Header Authorization: Bearer ...)

**Response Sukses (200 OK)**
Perhatikan struktur detail_produk yang sekarang memuat info nama barang & harga (Nested).
```
[
  {
    "kode_penjualan": "TRX-001",
    "nama_pembeli": "Sultan Andara",
    "tgl_transaksi": "2025-12-30T10:00:00",
    "detail_produk": [
      {
        "id_produk": 1,
        "jumlah": 2,
        "produk": {
          "nama_produk": "Cincin Emas 24K",
          "harga": 5000000
        }
      },
      {
        "id_produk": 5,
        "jumlah": 1,
        "produk": {
          "nama_produk": "Kalung Mutiara",
          "harga": 2500000
        }
      }
    ]
  }
]
```

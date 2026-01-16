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

#### Buat Transaksi Pembelian (NEW UPDATE)
- URL: /purchases
- Method: POST
 
**Skenario A: Restock Barang Lama**
Gunakan ini jika produk sudah ada di database (sudah punya ID), kita tinggal menambah stoknya saja.

**Request Body (JSON)**
```
{
  "id_produk": 1,
  "jumlah": 50,
  "harga_beli": 4000000,
  "nama_penjual": "Toko Emas Pusat",
  "no_hp_penjual": "08123456789"
}
```

**Skenario B: Beli Barang Baru**
Gunakan ini jika produk belum pernah ada di sistem. Backend akan otomatis membuatkan produk baru + kategori (jika valid) + stok awalnya.

Aturan:
- id_produk wajib diisi null.
- nama_produk_baru, kode_kategori_baru, dan harga_jual_baru (harga toko) WAJIB diisi.

**Request Body (JSON)**
```
{
  "id_produk": null,
  "nama_produk_baru": "Kalung Blue Diamond",
  "kode_kategori_baru": "KB",
  "harga_jual_baru": 6000000,
  "jumlah": 10,
  "harga_beli": 5500000,
  "nama_penjual": "jowney",
  "no_hp_penjual": "081299998888"
}
```

**Response Sukses (200 OK)**
```
{
  "kode_pembelian": 15,
  "tgl_transaksi": "2026-01-11T14:30:00",
  "nama_penjual": "Supplier Jakarta",
  "jumlah": 10,
  "produk": {
    "nama_produk": "Kalung Blue Diamond",
    "harga": 6000000
  }
}
```

Kemungkinan Error:
- 404 Not Found: Jika Restock Barang Lama tapi ID Produk salah.
- 404 Not Found: Jika Beli Barang Baru tapi kode_kategori_baru tidak ada di database (harus buat kategori dulu).
- 422 Unprocessable Entity: Format JSON salah (lupa koma, typo field).
 
#### Lihat Semua Riwayat Transaksi Pembelian (NEW UPDATE)
Endpoint ini digunakan untuk halaman "Laporan Pembelian". Data ditampilkan lengkap dengan nama barang yang terjual.
- URL: /purchases
- Method: GET
- Auth: Wajib Login (Butuh Header Authorization: Bearer ...)

**Response Sukses (200 OK)**
Perhatikan struktur detail_produk yang sekarang memuat info nama barang & harga.
```
[
  {
    "kode_pembelian": 1,
    "tgl_transaksi": "2026-01-11T14:35:59",
    "nama_penjual": "Jowney",
    "jumlah": 1,
    "produk": {
      "nama_produk": "Kalung Blue Diamond",
      "harga": 6000000
    }
  }
]
```
 
#### Predik Harga Berlian (NEW UPDATE)
- URL: /predict
- Method: POST

*Parameter Input***
| Parameter | Tipe  | Range | Keterangan                              |
|-----------|-------|-------|-----------------------------------------|
| carat     | Float | > 0.0 | Berat berlian (ct). Contoh: 0.5, 1.2.   |
| cut       | Int   | 1 - 5 | Kualitas Potongan (1: Fair, 5: Ideal).  |
| color     | Int   | 1 - 7 | Warna (1: J/Kuning, 7: D/Paling Putih). |
| clarity   | Int   | 1 - 8 | Kejernihan (1: I1, 8: IF/Sempurna).     |"

**Request Body (JSON)**
```
{
  "carat": 1.5,
  "cut": 5,
  "color": 6,
  "clarity": 7
}
```

**Response Sukses (200 OK)**
```
{
  "estimated_price": 15753424
}
```

Kemungkinan Error:
- Endpoint ini memuat file model (.pkl) dari folder server. Jika file model tidak ditemukan, harga akan bernilai 0.

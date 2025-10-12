# Blind Test Backend

FastAPI ile geliştirilmiş Blind Test uygulamasının backend servisi.

## Özellikler

- **Kullanıcı Yönetimi**: Admin ve Hakem rolleri
- **Model Yönetimi**: AI/LLM modellerinin entegrasyonu
- **Soru Havuzu**: Test sorularının organizasyonu
- **Test Yönetimi**: Blind test süreçlerinin yönetimi
- **Cevap Logları**: Model cevaplarının kaydı

## Teknolojiler

- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- Alembic (Migration)
- JWT Authentication
- Pydantic (Validation)

## Kurulum

### Gereksinimler

- Python 3.11+
- PostgreSQL
- Docker (opsiyonel)

### Yerel Kurulum

1. Repository'yi klonlayın:
```bash
git clone <repository-url>
cd blind_test_app
```

2. Virtual environment oluşturun:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\\Scripts\\activate  # Windows
```

3. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

4. Environment dosyasını oluşturun:
```bash
cp env.example .env
# .env dosyasını düzenleyin
```

5. PostgreSQL veritabanını oluşturun:
```sql
CREATE DATABASE blind_test_db;
```

6. Migration'ları çalıştırın:
```bash
alembic upgrade head
```

7. Uygulamayı başlatın:
```bash
uvicorn app.main:app --reload
```

### Docker ile Kurulum

```bash
docker-compose up --build
```

## API Dokümantasyonu

Uygulama çalıştıktan sonra:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Proje Yapısı

```
blind_test_app/
├── app/
│   ├── api/                 # API Router'lar
│   ├── core/               # Konfigürasyon ve güvenlik
│   ├── db/                 # Veritabanı modelleri ve CRUD
│   ├── schemas/            # Pydantic şemaları
│   ├── services/           # İş mantığı servisleri
│   └── main.py             # Ana uygulama
├── alembic/                # Migration dosyaları
├── tests/                  # Test dosyaları
└── requirements.txt        # Python bağımlılıkları
```

## Veritabanı Şeması

### Ana Tablolar

- **users**: Kullanıcı bilgileri (Admin/Hakem)
- **models**: AI/LLM model tanımları
- **input_pools**: Soru havuzları
- **questions**: Test soruları
- **tests**: Test tanımları
- **answer_logs**: Model cevaplarının logları

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Kullanıcı girişi
- `GET /api/v1/auth/me` - Mevcut kullanıcı bilgileri

### Admin
- `POST /api/v1/admin/users` - Kullanıcı oluşturma
- `POST /api/v1/admin/judges` - Hakem oluşturma
- `GET /api/v1/admin/users` - Kullanıcı listesi
- `POST /api/v1/admin/models` - Model oluşturma
- `POST /api/v1/admin/input-pools` - Soru havuzu oluşturma
- `POST /api/v1/admin/questions` - Soru oluşturma
- `POST /api/v1/admin/tests` - Test oluşturma

### Judges
- `GET /api/v1/judges/tests` - Aktif testler
- `POST /api/v1/judges/answer-logs` - Cevap logu oluşturma
- `GET /api/v1/judges/answer-logs` - Kendi cevap logları

### Tests
- `GET /api/v1/tests/tests` - Tüm testler
- `GET /api/v1/tests/models` - Aktif modeller
- `GET /api/v1/tests/input-pools` - Soru havuzları
- `GET /api/v1/tests/answer-logs` - Cevap logları

## Geliştirme

### Migration Oluşturma

```bash
alembic revision --autogenerate -m "Migration description"
alembic upgrade head
```

### Test Çalıştırma

```bash
pytest
```

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

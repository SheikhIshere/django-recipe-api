# Recipe API 🍳

A robust, well-tested RESTful API for managing recipes with full CRUD operations, authentication, and image uploads.

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![DRF](https://img.shields.io/badge/Django_REST-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **Authentication** | Token-based auth with custom email user model |
| 📝 **Recipe Management** | Full CRUD with image uploads & filtering |
| 🏷️ **Tag System** | Organize recipes with customizable tags |
| 🥗 **Ingredient System** | Manage recipe ingredients efficiently |
| 📚 **API Documentation** | Interactive Swagger/OpenAPI docs |
| 🐳 **Docker Ready** | Production-ready containerization |
| ✅ **Well Tested** | 1000+ lines of comprehensive tests |

## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose

### Installation

1. **Clone & Setup**
```bash
git clone <your-repo>
cd recipe_api
```

2. **Build & Run**
```bash
docker-compose build
docker-compose up
```

3. **Access the API**
- **API Documentation**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/
- **API Base**: http://localhost:8000/api/

4. **Create Superuser** (optional)
```bash
docker-compose run --rm app sh -c 'python manage.py createsuperuser'
```

## 📁 Project Structure

```
recipe_api/
├── App/
│   ├── core/                 # Project settings & config
│   ├── users/               # Custom user model & auth
│   ├── recipe/              # Recipe, Tag, Ingredient models
│   └── test/               # 1000+ lines of comprehensive tests
├── docker-compose.yml       # Multi-service setup
├── Dockerfile              # App container definition
└── requirements.txt        # Python dependencies
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/users/` | User registration |
| `POST` | `/api/users/token/` | Get auth token |
| `GET` | `/api/recipes/` | List recipes |
| `POST` | `/api/recipes/` | Create recipe |
| `GET` | `/api/recipes/{id}/` | Get recipe details |
| `PUT` | `/api/recipes/{id}/` | Update recipe |
| `DELETE` | `/api/recipes/{id}/` | Delete recipe |
| `GET/POST` | `/api/tags/` | Manage tags |
| `GET/POST` | `/api/ingredients/` | Manage ingredients |

## 🛠️ Development

### Running Tests
```bash
docker-compose run --rm app sh -c 'python manage.py test'
```

### Database Migrations
```bash
docker-compose run --rm app sh -c 'python manage.py migrate'
```

### Accessing Container Shell
```bash
docker-compose exec app sh
```

## 🎯 Key Features Deep Dive

### 🔐 Secure Authentication
- Custom user model with email authentication
- Token-based security for API access
- Protected endpoints with DRF permissions

### 📝 Advanced Recipe Management
- Image upload with UUID filename handling
- Many-to-many relationships with Tags & Ingredients
- Advanced filtering (`?tags=1,2`, `?ingredients=3`)
- `assigned_only` query parameter for clean responses

### ✅ Production Ready
- PostgreSQL for production database
- Docker containerization
- Comprehensive test suite
- Modular and scalable architecture

## 🚦 Example Usage

### Create Recipe
```http
POST /api/recipes/
Content-Type: application/json
Authorization: Token <your-token>

{
  "title": "Pasta Carbonara",
  "time_minutes": 30,
  "price": 12.50,
  "tags": [1, 2],
  "ingredients": [1, 3, 5]
}
```

### Filter Recipes
```http
GET /api/recipes/?tags=1&ingredients=3
```

## 📊 Testing Coverage

The project includes extensive testing with:
- ✅ Model tests
- ✅ API endpoint tests
- ✅ Authentication tests
- ✅ Serializer validation tests
- ✅ Image upload tests
- ✅ Filter and search tests

## 🔮 Future Enhancements

- [ ] Recipe rating system
- [ ] Advanced search with Elasticsearch
- [ ] Social features (sharing, comments)
- [ ] Meal planning functionality
- [ ] Recipe import from URLs

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Built with ❤️ using Django REST Framework | 100% Test Coverage**

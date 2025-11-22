# Recipe API 🍳

A robust and scalable RESTful API for managing recipes, ingredients, and tags. Built with Django REST Framework and designed for modern web and mobile applications.

## Features ✨

### 🔐 Authentication & User Management
- **Custom User Model** - Email-based authentication instead of username
- **Token-based Security** - Secure API access with token authentication
- **User CRUD Operations** - Complete user account management

### 📝 Recipe Management
- **Full CRUD Operations** - Create, read, update, and delete recipes
- **Image Upload Support** - Dynamic image handling with UUID-based filenames
- **Tag & Ingredient System** - Organize recipes with multiple tags and ingredients
- **Advanced Filtering** - Filter recipes by tags or ingredients

### 🏷️ Tag & Ingredient System
- **Independent Management** - Create, update, list, and delete tags/ingredients
- **Smart Filtering** - `assigned_only` query parameter for clean API responses

### 📚 API Documentation
- **OpenAPI/Swagger** - Fully integrated API documentation with drf-spectacular
- **Interactive Testing** - Test endpoints directly from the documentation

## Tech Stack 🛠️

**Backend:** Python, Django, Django REST Framework  
**Database:** PostgreSQL  
**Authentication:** Token-based with custom user model  
**Containerization:** Docker, Docker Compose  
**API Documentation:** drf-spectacular (OpenAPI/Swagger)  

## Quick Start 🚀

### Prerequisites
- Docker
- Docker Compose

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd recipe-api
```

2. **Start the application**
```bash
docker-compose up --build
```

3. **Access the application**
   - API: http://localhost:8000/api/
   - Admin Panel: http://localhost:8000/admin/
   - API Documentation: http://localhost:8000/api/docs/

## Project Structure 📁

```
recipe-api/
├── App/
│   ├── users/                 # User management app
│   │   ├── models.py         # Custom User model
│   │   ├── serializers.py    # User and Auth token serializers
│   │   ├── views.py          # User registration and management
│   │   └── admin.py          # Admin interface for users
│   ├── recipe/               # Recipe management app
│   │   ├── models.py         # Recipe, Tag, Ingredient models
│   │   ├── serializers.py    # Serializers for recipe objects
│   │   ├── views.py          # Recipe, tag, ingredient APIs
│   │   └── admin.py          # Admin interface for recipes
│   └── core/
│       └── settings.py       # Project configuration
├── docker-compose.yml        # Multi-container setup
├── Dockerfile               # App container definition
└── README.md               # Project documentation
```

## API Workflow 🔄

### 1. User Registration & Authentication
```http
POST /api/users/ - Register new user
POST /api/users/token/ - Obtain authentication token
```

### 2. Recipe Management
```http
GET    /api/recipes/          - List all recipes
POST   /api/recipes/          - Create new recipe
GET    /api/recipes/{id}/     - Retrieve specific recipe
PUT    /api/recipes/{id}/     - Update recipe
DELETE /api/recipes/{id}/     - Delete recipe
```

### 3. Tag & Ingredient Management
```http
GET    /api/tags/             - List tags
POST   /api/tags/             - Create tag
GET    /api/ingredients/      - List ingredients
POST   /api/ingredients/      - Create ingredient
```

### 4. Filtering Examples
```http
GET /api/recipes/?tags=1,2           - Filter by tag IDs
GET /api/recipes/?ingredients=3,4    - Filter by ingredient IDs
GET /api/tags/?assigned_only=1       - Show only assigned tags
```

## Key Design Principles 🎯

- **Reusability**: Base viewsets for tags/ingredients to minimize code duplication
- **Scalability**: Docker and PostgreSQL for production-ready deployment
- **Clean API**: Serializer-based logic following DRY principles
- **Security**: Token authentication with custom user model
- **Documentation**: Auto-generated OpenAPI/Swagger documentation

## Admin Panel 👨‍💼

Access the Django admin panel at `/admin/` to manage:
- Users and permissions
- Recipes, tags, and ingredients
- Database relationships and data integrity

## Development 🛠️

### Running without Docker
```bash
python manage.py migrate
python manage.py runserver
```

### Creating Superuser
```bash
docker-compose exec app python manage.py createsuperuser
```

### Running Tests
```bash
docker-compose exec app python manage.py test
```

## Future Enhancements 🔮

- [ ] Pagination for recipe lists
- [ ] Comprehensive unit and integration tests
- [ ] Caching for frequently accessed endpoints
- [ ] Advanced filtering (price, cooking time, search)
- [ ] Recipe rating and review system
- [ ] Social features (sharing, following users)

## Contributing 🤝

We welcome contributions! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ using Django REST Framework**

This App's aim to manage business-processes of home-based bakery
```
bakery
├─ .pre-commit-config.yaml
├─ Dockerfile
├─ LICENSE
├─ Makefile
├─ README.md
├─ bakery
│  ├─ __init__.py
│  ├─ __main__.py
│  ├─ adapters
│  │  ├─ __init__.py
│  │  └─ database
│  │     ├─ __init__.py
│  │     ├─ __main__.py
│  │     ├─ alembic.ini
│  │     ├─ base.py
│  │     ├─ config.py
│  │     ├─ converters
│  │     │  ├─ product.py
│  │     │  └─ user.py
│  │     ├─ di.py
│  │     ├─ migrations
│  │     │  ├─ env.py
│  │     │  ├─ script.py.mako
│  │     │  └─ versions
│  │     │     ├─ 2025_06_09_9d88c27af2f3_.py
│  │     │     └─ __init__.py
│  │     ├─ storages
│  │     │  ├─ __init__.py
│  │     │  ├─ product.py
│  │     │  └─ user.py
│  │     ├─ tables.py
│  │     ├─ uow.py
│  │     └─ utils.py
│  ├─ application
│  │  ├─ config.py
│  │  ├─ entities.py
│  │  └─ exceptions.py
│  ├─ config.py
│  ├─ domains
│  │  ├─ __init__.py
│  │  ├─ di.py
│  │  ├─ entities
│  │  │  ├─ __init__.py
│  │  │  ├─ common.py
│  │  │  ├─ order.py
│  │  │  ├─ product.py
│  │  │  └─ user.py
│  │  ├─ interfaces
│  │  │  ├─ __init__.py
│  │  │  └─ storages
│  │  │     ├─ __init__.py
│  │  │     ├─ product.py
│  │  │     └─ user.py
│  │  ├─ services
│  │  │  ├─ __init__.py
│  │  │  ├─ product.py
│  │  │  └─ user.py
│  │  ├─ uow.py
│  │  └─ utils
│  │     ├─ __init__.py
│  │     ├─ last_day_of_month_validator.py
│  │     └─ month_transformer.py
│  └─ presenters
│     ├─ __init__.py
│     └─ bot
│        ├─ __init__.py
│        ├─ commands
│        │  ├─ __init__.py
│        │  └─ utils.py
│        ├─ config.py
│        ├─ content
│        │  ├─ __init__.py
│        │  ├─ buttons
│        │  │  ├─ __init__.py
│        │  │  ├─ admin_main_menu.py
│        │  │  ├─ ask_question.py
│        │  │  ├─ catalogue
│        │  │  │  ├─ __init__.py
│        │  │  │  ├─ admin.py
│        │  │  │  ├─ common.py
│        │  │  │  └─ user.py
│        │  │  ├─ common.py
│        │  │  ├─ registration
│        │  │  │  ├─ __init__.py
│        │  │  │  └─ user.py
│        │  │  └─ user_main_menu.py
│        │  ├─ inline_query.py
│        │  ├─ links.py
│        │  └─ messages
│        │     ├─ __init__.py
│        │     ├─ catalogue
│        │     │  ├─ __init__.py
│        │     │  └─ common.py
│        │     ├─ exceptions.py
│        │     ├─ registration
│        │     │  ├─ __init__.py
│        │     │  ├─ main_menu.py
│        │     │  └─ user.py
│        │     └─ utils.py
│        ├─ di.py
│        ├─ dialogs
│        │  ├─ __init__.py
│        │  ├─ catalogue
│        │  │  ├─ __init__.py
│        │  │  ├─ admin
│        │  │  │  ├─ __init__.py
│        │  │  │  ├─ getters.py
│        │  │  │  ├─ handlers.py
│        │  │  │  ├─ selections.py
│        │  │  │  └─ windows.py
│        │  │  └─ windows.py
│        │  ├─ redirections.py
│        │  ├─ registration
│        │  │  ├─ __init__.py
│        │  │  └─ user
│        │  │     ├─ __init__.py
│        │  │     ├─ handlers.py
│        │  │     ├─ keyboards.py
│        │  │     └─ windows.py
│        │  ├─ states.py
│        │  └─ utils
│        │     └─ __init__.py
│        ├─ exception_handlers.py
│        ├─ filters
│        │  ├─ __init__.py
│        │  └─ role.py
│        ├─ keyboards
│        │  ├─ __init__.py
│        │  └─ main_menu.py
│        ├─ middlewares
│        │  ├─ __init__.py
│        │  ├─ middlewares.py
│        │  └─ user.py
│        ├─ router.py
│        ├─ service.py
│        ├─ services
│        │  └─ __init__.py
│        └─ utils
│           ├─ __init__.py
│           ├─ inline_query.py
│           └─ manager.py
├─ docker-compose.dev.yaml
├─ docker-compose.yaml
├─ docs
│  └─ db.puml
├─ poetry.lock
├─ pyproject.toml
└─ tests
   ├─ __init__.py
   ├─ adapters
   │  ├─ __init__.py
   │  └─ database
   │     ├─ __init__.py
   │     ├─ storages
   │     │  ├─ __init__.py
   │     │  ├─ test_product.py
   │     │  └─ test_user.py
   │     └─ test_migrations.py
   ├─ conftest.py
   ├─ domains
   │  ├─ __init__.py
   │  └─ services
   │     ├─ __init__.py
   │     ├─ test_product.py
   │     └─ test_user.py
   ├─ plugins
   │  ├─ __init__.py
   │  ├─ factories
   │  │  ├─ __init__.py
   │  │  ├─ product.py
   │  │  └─ user.py
   │  └─ instances
   │     ├─ __init__.py
   │     ├─ db.py
   │     ├─ services.py
   │     └─ storages.py
   └─ utils.py

```
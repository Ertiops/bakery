# 🧁 Bakery — Telegram Bot for Home Bakery Operations

A Telegram bot for managing a home bakery workflow: products, carts, pickup points, orders, payments, and delivery rules.
Built with clean architecture, async IO, and strong separation of concerns.

---

**✨ Features**
* ✅ Clean architecture with clear domain boundaries
* 🧩 Dependency Injection via Dishka
* 💬 Dialog-driven UX with `aiogram-dialog`
* 🔄 Redis-based FSM storage with TTL support
* 🛠️ PostgreSQL persistence via SQLAlchemy + Alembic
* 🧵 Transaction handling with Unit of Work
* ⏰ Scheduled cleanup jobs with aiomisc cron
* 🧪 Modular tests with pytest and factories
* 🧹 Static analysis with ruff and mypy
* 🐳 Docker + Makefile for local development

---

**🚀 Functional Overview**
* Product catalog management
* User carts and order creation
* Pickup address management
* Delivery schedule rules
* Order payments and totals
* Admin contacts and feedback group info
* Periodic cleanup of soft-deleted data

---

**⚙️ Development Setup**

Install dependencies:
```bash
make develop
```

Run dev containers:
```bash
make local
```

Stop dev containers:
```bash
make local_down
```

Start the bot:
```bash
make app
```

---

**📊 Migrations**
```bash
make local-create-migrations
make local-apply-migrations
make local-delete-migrations
```

---

**🧹 Code Quality**
```bash
make lint
make ruff
make mypy
```

---

**🧪 Testing**
```bash
make test
```

---

**🛠️ Environment Configuration**

Example `.env.dev`:
```env
APP_DB_USER=bakery
APP_DB_PASSWORD=bakery
APP_DB_NAME=bakery
APP_DB_HOST=localhost
APP_DB_PORT=5432

APP_REDIS_HOST=localhost
APP_REDIS_PORT=6379
APP_REDIS_PASSWORD=bakery

APP_TG_BOT_TOKEN=...
APP_TG_FSM_STATE_TTL=86400
APP_TG_FSM_DATA_TTL=86400
```

---

**📂 Project Structure**
```
bakery/
├─ adapters/       # DB, Redis, DI, storages, migrations
├─ application/    # Shared app config, exceptions
├─ domains/        # Entities, services, interfaces, utils
├─ presenters/     # Telegram bot: dialogs, handlers, messages
tests/             # Unit tests, factories, test utils
Makefile           # Development scripts
```

---

**🧑‍💻 Author**

Developed by Eljan T — straxisrule@gmail.com

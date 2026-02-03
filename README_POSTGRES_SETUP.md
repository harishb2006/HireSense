# PostgreSQL Setup for HireSense Mock Interview

## Quick Start

### 1. Start PostgreSQL Container

```bash
# From the project root directory
docker-compose up -d
```

This will:
- Pull PostgreSQL 16 Alpine image
- Create a container named `hiresense_postgres`
- Initialize the database with schema from `backend/database/init.sql`
- Expose PostgreSQL on port 5432

### 2. Verify Container is Running

```bash
docker ps | grep hiresense_postgres
```

### 3. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

Default database configuration:
```
DATABASE_URL=postgresql://hiresense_user:hiresense_password@localhost:5432/hiresense_db
```

## Database Schema

The database includes 4 main tables:

1. **user_profiles** - User information and statistics
2. **interview_sessions** - Interview session metadata and scores
3. **conversation_messages** - Complete conversation history
4. **question_bank** - Pre-defined questions with ideal answers

## Useful Commands

### Access PostgreSQL Shell

```bash
docker exec -it hiresense_postgres psql -U hiresense_user -d hiresense_db
```

### View Tables

```sql
\dt
```

### View Sample Questions

```sql
SELECT question_text, role, seniority_level FROM question_bank;
```

### Stop Container

```bash
docker-compose down
```

### Stop and Remove Data

```bash
docker-compose down -v
```

## Database Management

### Manual Schema Updates

If you need to modify the schema:

1. Update `backend/database/init.sql`
2. Recreate the database:

```bash
docker-compose down -v
docker-compose up -d
```

### Backup Database

```bash
docker exec hiresense_postgres pg_dump -U hiresense_user hiresense_db > backup.sql
```

### Restore Database

```bash
cat backup.sql | docker exec -i hiresense_postgres psql -U hiresense_user -d hiresense_db
```

## Connection Details

- **Host**: localhost
- **Port**: 5432
- **Database**: hiresense_db
- **Username**: hiresense_user
- **Password**: hiresense_password

## Troubleshooting

### Container won't start

Check logs:
```bash
docker-compose logs postgres
```

### Connection refused

Ensure container is running and healthy:
```bash
docker-compose ps
```

### Reset everything

```bash
docker-compose down -v
docker-compose up -d
```

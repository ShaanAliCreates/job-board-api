

up:
	docker compose up --build

down:
	docker compose down

down-v:
	docker compose down -v   

migrate:
	docker compose exec api alembic upgrade head

logs:
	docker compose logs -f api

shell:
	docker compose exec db psql -U jobuser -d jobboard
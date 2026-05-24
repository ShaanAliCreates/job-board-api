up:
	docker compose up --build
down:
	docker compose down

down-v:
	docker compose down -v

migrate:
	docker compose exec api alembic head upgrade

logs:
	docker compose logs -f api

shell:
	docker compose exec db -U postgres -d jobboard
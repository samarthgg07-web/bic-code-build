.PHONY: help install setup run dev clean test format lint security

help:
	@echo "Code, Bid & Build - Development Commands"
	@echo "=========================================="
	@echo "make install    - Install dependencies"
	@echo "make setup      - Run initial setup"
	@echo "make run        - Run production server"
	@echo "make dev        - Run development server"
	@echo "make clean      - Clean up temporary files"
	@echo "make test       - Run tests"
	@echo "make format     - Format code with black"
	@echo "make lint       - Run code linting"
	@echo "make security   - Check security issues"
	@echo "make docker     - Build Docker image"
	@echo "make docker-run - Run with Docker"

install:
	pip install -r requirements.txt

setup:
	python setup.py

run:
	gunicorn -w 4 -b 0.0.0.0:5000 app:app

dev:
	python app.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".DS_Store" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

test:
	pytest tests/ -v

format:
	black app.py config.py setup.py

lint:
	pylint app.py config.py

security:
	bandit -r . -ll

docker:
	docker build -t codebiduild:latest .

docker-run:
	docker run -p 5000:5000 codebiduild:latest

.DEFAULT_GOAL := help

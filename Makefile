start_tests:
	@echo 'Start docker-compose'
	@cd .docker && ./start.sh

run_tests:
	@echo 'Running tests, containers must be running'
	@cd .docker && ./exec.sh

stop_tests:
	@echo 'Stopping/killing containers'
	@cd .docker && ./stop.sh

tests: start_tests run_tests stop_tests

github-pages:
	@docker run --rm -w /plugin -v $(shell pwd):/plugin 3liz/pymarkdown:latest docs/README.md docs/index.html
	@docker run --rm -w /plugin -v $(shell pwd):/plugin 3liz/pymarkdown:latest docs/dev/README.md docs/dev/index.html

processing-doc:
	cd .docker && ./processing_doc.sh
	docker run --rm -w /plugin -v $(shell pwd):/plugin 3liz/pymarkdown:latest docs/processing/README.md docs/processing/index.html

reset: configured
	@rm configured
	@cp default_config.yaml config.yaml

reset_conf:
	@cp default_config.yaml config.yaml

clear_logs:
	@rm ./log/*.log
	@echo "Logs cleared"

clean:
	rm reset
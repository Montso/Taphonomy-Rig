reset: configured
	@rm configured
	@cp default_config.yaml config.yaml
	@echo "Out-Of-The-Box reset."

reset_conf:
	@cp default_config.yaml config.yaml
	@echo "Default configurations set."

clear_logs:
	@rm ./log/*.log
	@echo "Logs cleared"

.DEFAULT:reset_conf
from configuration.configuration import server_config as config

print config.get('mongodb', 'host')
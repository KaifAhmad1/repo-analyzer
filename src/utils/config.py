def load_config():
    """
    Load application configuration. Returns a dictionary with at least 'app' key containing 'name' and 'version'.
    This is a default implementation since YAML config files were removed.
    """
    return {
        "app": {
            "name": "GitHub Repository Analyzer",
            "version": "1.0.0"
        },
        # Add other default config sections here as needed
    } 
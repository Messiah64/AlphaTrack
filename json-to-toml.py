import toml

output = ".streamlit/secrets.toml"

with open("service.json") as json_file:
    json_key = json_file.read()

config = {"textkey": json_key}
toml_config = toml.dumps(config)

with open(output, "w") as f:
    f.write(toml_config)
    print("success")

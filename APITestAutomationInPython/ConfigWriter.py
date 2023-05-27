from configparser import ConfigParser

config = ConfigParser()

config["Default"] = {
    "EmailUsername": "abdul@finboa.com",
    "EmailPassword": "$Pak35tan$2027",
    "ApplicationUsername": "abdul@finboa.com",
    "ApplicationPassword": "Password@5",
    "FinboaSSOURL": "https://finboasso.azurewebsites.net/",
    "DisputeDevAPIURL": "https://disputedevapi.azurewebsites.net",
    "DisputeDevURL": "https://disputedev.azurewebsites.net",
    "FinboaAccountV3": "https://finboaaccountv3.azurewebsites.net/",
    "FinboaAccountAPIV3": "https://finboaaccountapiv3.azurewebsites.net"
}


with open("FinboaConfig.ini", "w") as f:
    config.write(f)
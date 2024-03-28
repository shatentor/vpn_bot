
## Telegram bot for managing PiVPN WireGuard clients.

## Description 
Allows you to get your own VPN service ! 
After PiVPN installation on your remote server, through this bot you can create or delete clients, get configuration files with qr-codes.
Allso other users can get VPN configs if they have a password ;) . 
Bot makes your work with PiVPN more easier and more convinient.


## Instlallation
1. In case you have your personal server (if no, you should to get one), you need to install WireGuard and PiVPN:
   - sudo apt update
   - sudo apt upgrade
   - sudo apt install wireguard
   - curl -L https://install.pivpn.io | bash
   
The PiVPN installation wizard will guide you through the setup process. Follow the prompts to configure WireGuard and PiVPN according to your preferences.
Aslo start WireGuard Service if it`s not already running:
   - sudo systemctl start wg-quick@wg0

Additionally, enable the service to start on boot:
   - sudo systemctl enable wg-quick@wg0
     
2. Clone repository:
  - git clone https://github.com/shatentor/vpn_bot.git
  - cd vpn_bot

3. Install requirements:
  - pip install -r requirements.txt
    
4. Update file "config.py" with your token Telegram API.
5. Here I use MariaDB to store all data (becuse I worked with it at University). To install:
   - sudo apt install mariadb-server
   - sudo systemctl start mariadb
   - sudo systemctl enable mariadb
     
   Now you need to instal template of tables that I use:

   CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255),
    gained_access TIMESTAMP ,
    current_pass VARCHAR(255),
    chat_id VARCHAR(255),
    number_of_configs INT
);

   CREATE TABLE IF NOT EXISTS configs_dates (
    username VARCHAR(255),
    config_1 DATETIME,
    config_2 DATETIME,
    config_3 DATETIME,
    config_4 DATETIME,
    chat_id INT
);

6. Update file "mariadb_conn.py" with your data.
7. Update "admin_commads.py" with your admin nickname.


## Usage
There are two types of users in bot: admin and other users.
Admin can ![do this commands](https://drive.google.com/file/d/13FQLFD-mTLCYMhJuE7pBaaz5h02Zjoxi/view?usp=drivesdk) 
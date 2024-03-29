
# Telegram bot for managing PiVPN WireGuard clients.

## Description 
Manage your own VPN service with ease! After installing PiVPN on your remote server,
you can create and delete clients, and obtain configuration files with QR codes through 
this bot. Additionally, other users can access VPN configurations with a password, 
enhancing convenience and accessibility.

## Instlallation
1. In case you have your personal server (if no, you should to get one), you need to install WireGuard and PiVPN:
    ```
   sudo apt update
   sudo apt upgrade
   sudo apt install wireguard
   curl -L https://install.pivpn.io | bash
   ```
   
2. The PiVPN installation wizard will guide you through the setup process. Follow the prompts to configure WireGuard and PiVPN according to your preferences.
Also start WireGuard Service if it is not already running:
   ```
   sudo systemctl start wg-quick@wg0
   ```
   
    Additionally, enable the service to start on boot:
    ```        
    sudo systemctl enable wg-quick@wg0
    ```     

3. Clone repository:
    ```
    git clone https://github.com/shatentor/vpn_bot.git
    cd vpn_bot
    ```
4. Install requirements:
    ```
    pip install -r requirements.txt
    ```
   
5. Update file "config.py" with your token Telegram API.
6. Here I use MariaDB to store all data (becuse I worked with it at University). To install:
   ```
   sudo apt install mariadb-server
   sudo systemctl start mariadb
   sudo systemctl enable mariadb
   ```  
   Now you need to create template of tables that I use:

    ```
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
    ```
7. Update file "mariadb_conn.py" with your data.
8. Update file "admin_commads.py" with your admin nickname.
9. Update [wg_config_path](main_stucture/generate_sens_qr.py) with yours in file "generate_send_qr.py".


## Usage
There are two types of users in bot: admin and other users.

### Administrator Commands:![admin_commands](stuff_for_readme/admin_commands.png)
Admin can get any configuration by its name: "Config + QR-code"


### Other User Commands: ![users_commands](stuff_for_readme/other_users_commands.png)

   User can get new config after entering the password (admin have it) or can get all his configurations:
![all_configs](stuff_for_readme/all_configs.png)

  
## License 
This project licenced by Apache License Version 2.0 - look file [LICENSE](LICENSE).

## Contribution 
Contributions to the project are welcome! 
Feel free to report bugs or suggest improvements. Collaboration with other developers or 
receiving advice is also appreciated.

## Contact 
You can reach me via email at shatentor66@gamil.com.
## Project Status 
This project is currently under development.


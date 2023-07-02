<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<br />
<div align="center">
  <a href="https://github.com/richardokonicha/tg-marketplace">
    <img width="50" height="50" src="https://img.icons8.com/3d-fluency/94/commodity.png" alt="commodity"/>
    <img width="188" height="188" src="https://img.icons8.com/3d-fluency/188/telegram.png" alt="telegram"/>
    <img width="50" height="50" src="https://img.icons8.com/3d-fluency/94/blockchain.png" alt="blockchain"/>
  </a>
  <br />
  <br />
  <h3 align="center"> <strong>Telegram Bot Marketplace</strong></h3>

  <p align="center">
    A Telegram bot that allows you to buy and sell items in a marketplace.
    </>
    <br />
    <a href="https://github.com/richardokonicha/tg-marketplace/">View Demo</a>
    ·
    <a href="https://github.com/richardokonicha/tg-marketplace/issues">Report Bug</a>
    ·
    <a href="https://github.com/richardokonicha/tg-marketplace/issues">Request Feature</a>
  </p>

  <br />

  <div align="center">
    <a href="https://github.com/richardokonicha/tg-marketplace">
      <img src="images/menu.png" alt="Logo" width="200" height="200">
    </a>
    <a href="https://github.com/richardokonicha/tg-marketplace">
      <img src="images/multilang.png" alt="Logo" width="200" height="200">
    </a>
    <a href="https://github.com/richardokonicha/tg-marketplace">
      <img src="images/menu2.png" alt="Logo" width="200" height="200">
    </a>
    <a href="https://github.com/richardokonicha/tg-marketplace">
      <img src="images/invoice.png" alt="Logo" width="200" height="200">
    </a>
  </div>

</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

This Bot is a telegram marketplace bot, It supports 3 kind of users,

- Regular user privileges
  - Can view products and categories
  - Can Buy products using BTC or LTC
  - Can Credit wallet using BTC or LTC
  - Can Buy products from wallet balance
  - Can view purchase history
  - Can message Group Admin

##

- Vendor user privileges

  - Can Create new products
  - Can Create new category
  - Can receive credit from product sales
  - Can request Funds withdrawal
  - Can view products and categories
  - Can Buy products using BTC or LTC
  - Can Credit wallet using BTC or LTC
  - Can Buy products from wallet balance
  - Can view purchase history
  - Can message Group Admin

- Admin user privilege
  - All of the above
  - Can access dashboard to view all users, vendors, purchases, deposits, withdrawals
  - Can promote a user from regular user to vendor
  - Can demote a vendor to regular user
  - Can delete a product
  - Can delete a category
  - Can view all users, vendors, purchases, deposits, withdrawals
  - Can message all users

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [![Python][Python-img]][Python-url]
- [![Flask][Flask-img]][Flask-url]
- [![MongoDB][MongoDB-img]][MongoDB-url]
- [![BTCPay][BTCPay-img]][BTCPay-url]
- [![Telegram API][Telegram-API-img]][Telegram-API-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get this project copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

- Python
  ```sh
  pip install -r requirements.txt
  ```

## Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a telegram bot API Key at [telegram bot tutorial](https://core.telegram.org/bots/tutorial)
2. Clone the repo
   ```sh
   git clone https://github.com/richardokonicha/tg-marketplace.git
   ```
3. Install NPM packages
   ```sh
   pip install -r requirements.txt
   ```
4. Enter your environment in `.env`
   ```js
    TOKEN=********:***********-Avkvvk7wA*****
    ADMIN=577180091
    CURRENCY=BTC
    FIAT_CURRENCY=USD
    DATABASE_URL=mongodb+srv://user:pass@cluster.mongodb.net/
    WEBHOOK_URL = https://your_server_url.app
    WEBHOOKMODE = True
    BTCPAY_STORE_ID=B5HeoVS****************************
    BTCPAY_TOKEN=2218e3892f***************************
    BTCPAY_SERVER=https://btcpay.your_btcpay_server.com
   ```
5. Run the bot
   ```sh
   python main.py
   ```

### Docker

1. Clone the repo
   ```sh
   git clone https://github.com/richardokonicha/tg-marketplace.git
   ```
2. Install docker
   ```sh
   sudo apt-get install docker.io
   ```
3. Install docker-compose
   ```sh
   sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local
   compose
   sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
   ```
4. Enter your Environment variables in `.env`
   ```js
    TOKEN=********:***********-Avkvvk7wA*****
    ADMIN=577
    CURRENCY=BTC
    FIAT_CURRENCY=USD
    DATABASE_URL=mongodb+srv://user:pass@cluster.mongodb.net/
    WEBHOOK_URL = https://your_server_url.app
    WEBHOOKMODE = True
    BTCPAY_STORE_ID=B5HeoVS****************************
    BTCPAY_TOKEN=2218e3892f***************************
    BTCPAY_SERVER=https://btcpay.your_btcpay_server.com
   ```
5. Run the bot
   ```
   docker-compose up -d
   ```

For addition configuration options, check `config.js` file

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/richardokonicha/tg-marketplace.svg?style=for-the-badge
[contributors-url]: https://github.com/richardokonicha/tg-marketplace/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/richardokonicha/tg-marketplace.svg?style=for-the-badge
[forks-url]: https://github.com/richardokonicha/tg-marketplace/network/members
[stars-shield]: https://img.shields.io/github/stars/richardokonicha/tg-marketplace.svg?style=for-the-badge
[stars-url]: https://github.com/richardokonicha/tg-marketplace/stargazers
[issues-shield]: https://img.shields.io/github/issues/richardokonicha/tg-marketplace.svg?style=for-the-badge
[issues-url]: https://github.com/richardokonicha/tg-marketplace/issues
[license-shield]: https://img.shields.io/github/license/richardokonicha/tg-marketplace.svg?style=for-the-badge
[license-url]: https://github.com/richardokonicha/tg-marketplace/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/richardokonicha
[product-screenshot]: images/screenshot.png
[Python]: https://img.shields.io/badge/python-000000?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org/
[Tailwindcss.com]: https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white
[Tailwindcss-url]: https://tailwindcss
[Python-img]: https://img.shields.io/badge/Python-000000?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org/
[Flask-img]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://palletsprojects.com/p/flask/
[MongoDB-img]: https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white
[MongoDB-url]: https://www.mongodb.com/
[BTCPay-img]: https://img.shields.io/badge/BTCPay-FF6C2C?style=for-the-badge&logo=btcpay&logoColor=white
[BTCPay-url]: https://btcpayserver.org/
[Telegram-API-img]: https://img.shields.io/badge/Telegram%20API-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white
[Telegram-API-url]: https://core.telegram.org/api

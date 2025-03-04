# richat-test

<!-- PROJECT LOGO -->
<div align="center">
  <h2>richat-test</h2>

  <h3 align="center">README тестового задания</h3>

  <p align="center">
    stripe.com/docs - платёжная система с подробным API и бесплатным тестовым режимом для имитации и тестирования платежей.
    С помощью python библиотеки stripe можно удобно создавать платежные формы разных видов, сохранять данные клиента, и реализовывать прочие платежные функции. 
  </p>
</div>

<a name="readme-top"></a>

<hr>

<!-- ABOUT THE PROJECT -->
## About The Project

Требования:
Реализовать Django + Stripe API бэкенд со следующим функционалом и условиями:
* Django Модель Item с полями (name, description, price) 
* API с двумя методами:
  * GET /buy/{id}, c помощью которого можно получить Stripe Session Id для оплаты выбранного Item. При выполнении этого метода c бэкенда с помощью python библиотеки stripe должен выполняться запрос stripe.checkout.Session.create(...) и полученный session.id выдаваться в результате запроса
  * GET /item/{id}, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном Item и кнопка Buy. По нажатию на кнопку Buy должен происходить запрос на /buy/{id}, получение session_id и далее  с помощью JS библиотеки Stripe происходить редирект на Checkout форму stripe.redirectToCheckout(sessionId=session_id)
* Залить решение на Github, описать запуск в Readme.md
* Опубликовать свое решение онлайн, предоставив ссылку на решение и доступ к админке, чтобы его можно было быстро и легко протестировать. 

Бонусные задачи: 
* Запуск используя Docker
* Использование environment variables
* Просмотр Django Моделей в Django Admin панели
* Запуск приложения на удаленном сервере, доступном для тестирования, с кредами от админки
* Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items
* Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме. 
* Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте
* Реализовать не Stripe Session, а Stripe Payment Intent.


### Built With

* [![Django][Django-badge]][Django-url]
* [![Postgres][Postgres-badge]][Postgres-url]
* [![Docker][Docker-badge]][Docker-url]
* [![Bootstrap][Bootstrap-badge]][Bootstrap-url]
* [![JQuery][JQuery-badge]][JQuery-url]


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Copy project to repository on local machine (HTTPS or SSH)
  ```sh
  git clone https://github.com/SuperLalka/richat-test.git
  ```
  ```sh
  git clone git@github.com:SuperLalka/richat-test.git
  ```

### Installation

To start the project, it is enough to build and run docker containers.
Database migration and fixture loading will be applied automatically.

```sh
docker build -t rc_django . && docker run -it rc_django
```

### Documentation

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Django-badge]: https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://docs.djangoproject.com/
[Postgres-badge]: https://img.shields.io/badge/postgresql-%234169E1.svg?style=for-the-badge&logo=postgresql&logoColor=white
[Postgres-url]: https://www.postgresql.org/
[Docker-badge]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[Bootstrap-badge]: https://img.shields.io/badge/bootstrap-%237952B3.svg?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com/
[JQuery-badge]: https://img.shields.io/badge/jquery-%230769AD.svg?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com/

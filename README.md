# hack-BV
## Introduction
A super cool service which integrates BlendVision API and other third-party tools to provide streaming service
## Install
### requirements
- docker
- docker-compose
- make
### step 1
After you have all your requirements installed, you can use the following command to build up this project
```
$ sudo make build
```
*first time build will take some time*
If the project has been built up successfully, you should something like this
```
 => => naming to docker.io/library/python-bv                                                                           0.0s
[+] Running 4/4
 ✔ Network hack-bv_BV-networks  Created                                                                                0.0s 
 ✔ Container go-linebot         Started                                                                                0.4s 
 ✔ Container backend            Started                                                                                0.2s 
 ✔ Container ngrok              Started  
```
### step 2
Now you can goto [Line developers](https://developers.line.biz/en/) and register your LineBot
Then open http://127.0.0.1:4040/ in your web browser, you should see an url provided by ngrok
Copy and paste the url into webhook url (don't forget the /callback route)
### step 3
You can use Postman or Curl to test your API
For backend API, the following API should work immediately after you build up the project
```
$ curl -i http://127.0.0.1:8090/welcome
HTTP/1.1 200 OK
Server: Werkzeug/2.3.7 Python/3.11.5
Date: Fri, 29 Sep 2023 14:40:40 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 12
Connection: close

hello, world%
```
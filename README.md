Check  balance of  selectel accounts and receive notifications in the telegram


### Install

```
git clone https://github.com/DorofD/selectel_balance_checker && \
cd selectel_balance_checker && \
cp app/conf.example.json app/conf.json
```
Set your environment variables in app/conf.json
```
docker build -t selectel_balance_checker . 
docker run -d -v ./app/conf.json:/app/conf.json selectel_balance_checker
```

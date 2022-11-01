# Bash/Python scripting
* Общее количество запросов (1 балл)
* Общее количество запросов по типу, например: GET - 20, POST - 10 и т.д. (1 балл)
* Топ 10 самых частых запросов (1 балл):
  * должен выводиться url
  * должно выводиться число запросов
* Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой (1 балл):
  * должен выводиться url
  * должен выводиться статус код
  * должен выводиться размер запроса
  * должен выводиться ip адрес
* Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой (1 балл):
  * должен выводиться ip адрес
  * должно выводиться количество запросов
## Bash
Код находится в _[nginx_parser.sh](nginx_parser.sh)_

Результат записывается в файл _[res_bash.txt](res_bash.txt)_
### 1 задание
```sh
echo "Total number of requests:" > "$RES_FILE"
wc -l "$LOG_FILE" | awk '{print $1}' >> "$RES_FILE"
```
С помощью `wc -l` получаем количество строк в файле с логами и записываем его в результат
### 2 задание
```sh
echo -e "\nTotal number of requests by type:" >> "$RES_FILE"
awk '{print $6}' "$LOG_FILE" | tr -d \" | sed '/^.\{100\}./d' | \
sort | uniq -c | sort -rn | awk '{printf "%s - %d\n", $2, $1}' >> "$RES_FILE"
```
* Считываем тип запроса (6 столбик) из логов - `awk '{print $6}' "$LOG_FILE"`
* Удаляем кавычку, удаляем артефакт с длиной > 100 символов - `tr -d \" | sed '/^.\{100\}./d'`
* Оставляем уникальные значения складывая количество, сортируем по убыванию - `sort | uniq -c | sort -rn`
* Записываем в результат - `awk '{printf "%s - %d\n", $2, $1}' >> "$RES_FILE"`
### 3 задание
```sh
echo -e "\nTop 10 most frequent requests:" >> "$RES_FILE"
awk '{print $7}' "$LOG_FILE" | sed 's/^.*:\/\/[^\/]*//' | \
sort | uniq -c | sort -rnk1 | head | awk '{printf "PATH: %s\nNumber of requests: %d\n-\n", $2, $1}' >> "$RES_FILE"
```
* Считываем URL (path) запроса (7 столбик) из логов - `awk '{print $7}' "$LOG_FILE"`
* Убираем часть с адресом страницы - `sed 's/^.*:\/\/[^\/]*//'`
* Оставляем уникальные значения складывая их количество, сортируем по убыванию, берём первые 10 значений - `sort | uniq -c | sort -rnk1 | head`
* Записываем в файл с результатами - `awk '{printf "PATH: %s\nNumber of requests: %d\n-\n", $2, $1}' >> "$RES_FILE"`
### 4 задание
```sh
echo -e "\nTop 5 largest requests with (4XX) error:" >> "$RES_FILE"
awk '{if ($9 ~ /4../) print $7, $9, $10, $1}' "$LOG_FILE" | \
sort -rnk3 | head -n 5 | awk '{printf "PATH: %s\nResponse code: %d\nSize: %d\nIP: %s\n-\n", $1, $2, $3, $4}' >> "$RES_FILE"
```
* Считываем URL (path), код ответа, размер и IP запросов из логов, если код ответа == 4xx - `awk '{if ($9 ~ /4../) print $7, $9, $10, $1}' "$LOG_FILE"`
* Сортируем по размеру, берем первые 5 значений - `sort -rnk3 | head -n 5`
* Записываем в файл с результатами - `awk '{printf "PATH: %s\nResponse code: %d\nSize: %d\nIP: %s\n-\n", $1, $2, $3, $4}' >> "$RES_FILE"`
### 5 задание
```sh
echo -e "\nTop 5 users by number of requests with (5XX) error:" >> "$RES_FILE"
awk '{if ($9 ~ /5../) print $1}' "$LOG_FILE" | \
sort | uniq -c | sort -rnk1 | head -n 5 | awk '{printf "IP: %s\nNumber of requests: %d\n-\n", $2, $1}' >> "$RES_FILE"
```
* Считываем IP запросов из логов, если код ответа == 5xx - `awk '{if ($9 ~ /5../) print $1}' "$LOG_FILE"`
* Оставляем уникальные значения складывая их количество, сортируем по убыванию, берем первые 5 значений - `sort | uniq -c | sort -rnk1 | head -n 5`
* Записываем в файл с результатами - `awk '{printf "IP: %s\nNumber of requests: %d\n-\n", $2, $1}' >> "$RES_FILE"`
### Минусы и плюсы решения
#### Минусы
* Необходимость хорошего знания синтаксиса команд
* Сложность запуска на Windows
#### Плюсы
* Скрипты в несколько строчек
## Python
Код находится в _[nginx_parser.py](nginx_parser.py)_

Результат записывается в файл _[res_py.txt](res_py.txt)_ или в файл _[res_py.json](res_py.json)_, если указан флаг `--json`
### 2 задание
```
req_by_type = [request.split()[5][1:] for request in
                self.log_file.readlines() if
                len(request.split()[5][1:]) < 100]
req_by_type = Counter(req_by_type).most_common()
self.log_file.seek(0)

if self.json:
    self.json_info["Number of requests by type"] = {
        req_type[0]: req_type[1] for req_type in req_by_type}
else:
    self.res_file.write('Total number of requests by type:\n')
    self.res_file.writelines(
        [f'{req_type[0]} - {req_type[1]}\n' for req_type in req_by_type])
```
* Построчно считываем тип запроса из логов (6 столбец), убирая первую кавычку и отсеиваем артефакт с длиной > 100 - `request.split()[5][1:] for request in self.log_file.readlines() if len(request.split()[5][1:]) < 100`
* Считаем количество вхождений каждого типа и сортируем их по убыванию - `req_by_type = Counter(req_by_type).most_common()`
* В зависимости от флага `--json` записываем результат в нужный файл в нужном формате
### 3 задание
```
req_by_url = [re.sub(r'^.*://[^/]*', '', request.split()[6]) for request in
                      self.log_file.readlines()]
req_by_url = Counter(req_by_url).most_common(10)
self.log_file.seek(0)

if self.json:
    self.json_info["Top 10 most frequent requests"] = [
        {"PATH": request[0], "Number of requests": request[1]} for
        request in req_by_url]
else:
    self.res_file.write('\nTop 10 most frequent requests:')
    self.res_file.writelines(
        [f'\nPATH: {request[0]}\nNumber of requests: {request[1]}\n-' for
         request in req_by_url])
```
* Построчно считываем URL (path) запроса из логов, убирая часть с адресом страницы - `req_by_url = [re.sub(r'^.*://[^/]*', '', request.split()[6]) for request in self.log_file.readlines()]`
* Считаем количество вхождений каждого path, сортируем их по убыванию и оставляем первые 10 - `req_by_url = Counter(req_by_url).most_common(10)`
* В зависимости от флага `--json` записываем результат в нужный файл в нужном формате
### 5 задание
```
ip_5xx = [request.split()[0] for request in self.log_file.readlines() if
                    re.match(r'5\d{2}', request.split()[8])]
freq_ip = Counter(ip_5xx).most_common(5)
self.log_file.seek(0)

if self.json:
    self.json_info["Top 5 users by number of requests with (5XX) error"] = [
        {"IP": ip[0], "Number of requests": ip[1]} for
        ip in freq_ip]
else:
    self.res_file.write(
        '\n\nTop 5 users by number of requests with (5XX) error:')
    self.res_file.writelines(
        [f'\nIP: {ip[0]}\nNumber of requests: {ip[1]}\n-' for ip in
         freq_ip])
```
* Построчно считываем IP пользователя, если запрос завершился ошибкой (5XX) - `ip_5xx = [request.split()[0] for request in self.log_file.readlines() if re.match(r'5\d{2}', request.split()[8])]`
* Считаем количество вхождений каждого IP, сортируем их по убыванию и оставляем первые 5 - `freq_ip = Counter(ip_5xx).most_common(5)`
* В зависимости от флага `--json` записываем результат в нужный файл в нужном формате
### Минусы и плюсы решения
#### Минусы
* Более объёмный код
#### Плюсы
* Проще читать код
* Проще запускать на разных платформах
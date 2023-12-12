# practice3 Гарбузов Павел БСБО-01-20
## Задание 1: файл password_bruteforce.py
## Задание 3: файлы auth.py, bruteforce_auth.py
---
## Задание 2:
``` php
if( isset( $_GET[ 'Login' ] ) ) {
        // Get username
        $user = $_GET[ 'username' ];
        // Get password
        $pass = $_GET[ 'password' ];
        $pass = md5( $pass );
        // Check the database
        $query  = "SELECT * FROM `users` WHERE user = '$user' AND password = '$pass';";
        $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );
        if( $result && mysqli_num_rows( $result ) == 1 ) {
                // Get users details
                $row    = mysqli_fetch_assoc( $result );
                $avatar = $row["avatar"];
                // Login successful
                $html .= "<p>Welcome to the password protected area {$user}</p>";
                $html .= "<img src=\"{$avatar}\" />";
        }
        else {
                // Login failed
                $html .= "<pre><br />Username and/or password incorrect.</pre>";
        }
        ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
}
```
## Уязвимости:
* CWE-79

Недостаточная нейтрализация ввода при генерации веб-страницы ('Cross-site Scripting' или 'Межсайтовый скриптинг'): Код напрямую использует переменную $user в HTML-выводе, что может стать вектором атак XSS, если имя пользователя не санитизировано должным образом.
*CWE-89

Недостаточная нейтрализация специальных элементов, используемых в SQL-команде ('SQL-инъекция'): Код включает данные, контролируемые пользователем ($user и $pass), в SQL-запрос, что делает его уязвимым для SQL-инъекций. Это особенно критично, так как имя пользователя не санитизируется перед встраиванием в SQL-запрос.
*CWE-598

Использование метода GET для передачи чувствительных данных: Использование $_GET для передачи имени пользователя и пароля является риском для безопасности, потому что URL-адреса регистрируются в истории браузера, серверных логах и могут быть раскрыты через заголовки Referer в HTTP-запросах.
*CWE-759

Использование одностороннего хеша без соли: MD5 используется без соли, что делает систему уязвимой для атак с использованием радужных таблиц.
*CWE-732

Некорректное назначение прав для критически важных ресурсов: Отрывок показывает, что код выполняет SQL-запросы, что предполагает, что PHP-код может выполняться с слишком широкими разрешениями, потенциально позволяя выполнять непреднамеренные запросы.
*CWE-523

Незащищенная передача учетных данных: Учетные данные могут передаваться по незащищенному соединению, если не использовать HTTPS, что делает их уязвимыми для атак перехвата.
*CWE-311

Отсутствие шифрования чувствительных данных: Хотя это и не указано непосредственно в отрывке кода, отсутствие упоминания о каком-либо защищенном слое передачи подразумевает, что учетные данные могут передаваться по сети без шифрования, что делает их уязвимыми для перехвата.
*CWE-200

Раскрытие конфиденциальной информации неуполномоченному лицу: Если имя пользователя верно, но пароль неверен, сообщение указывает на то, что имя пользователя существует. Эту информацию можно использовать для дальнейших атак.
*CWE-302

Обход аутентификации путем предположения неизменяемости данных: Код предполагает, что запрос к базе данных, возвращающий одну строку, достаточен для аутентификации, без дополнительных проверок состояния аутентификации пользователя или его привилегий.

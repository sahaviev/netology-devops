# 3.2. Работа в терминале, лекция 2

### 1. Какого типа команда cd? Попробуйте объяснить, почему она именно такого типа; опишите ход своих мыслей, если считаете что она могла бы быть другого типа.

Изначально я думал что она stdin-типа.
Я пытался связать каким именно образом она принимает на вход данные и меняет **work directory**.
Но ее нельзя использовать в pipe. 

Почитав комменты понял что это часть shell'a. По факту я так понял что команда **cd /directory** идут как параметры 
shell'a.

```console
vagrant@vagrant:~$ type cd
cd is a shell builtin
```


### 2. Какая альтернатива без pipe команде grep <some_string> <some_file> | wc -l?

Можно так:

```commandline
grep . test.txt -c
```

Можно так:

```commandline
cat test.txt | grep . -c
```


### 3. Какой процесс с PID 1 является родителем для всех процессов в вашей виртуальной машине Ubuntu 20.04?

Не уверен что я правильно отвечаю, но вроде как логично что это процесс **systemd**

Можно узнать через дерево всех процессов(**pstree**):

```console
vagrant@vagrant:~$ pstree -p
systemd(1)─┬─VBoxService(795)─┬─{VBoxService}(797)
           │                  ├─{VBoxService}(798)
           │                  ├─{VBoxService}(799)
           │                  ├─{VBoxService}(800)
           │                  ├─{VBoxService}(801)
           │                  ├─{VBoxService}(802)
           │                  ├─{VBoxService}(803)
           │                  └─{VBoxService}(804)
           ├─accounts-daemon(597)─┬─{accounts-daemon}(625)
           │                      └─{accounts-daemon}(651)
...
```

Через команду **ps**:
```console
vagrant@vagrant:~$ ps -p 1
    PID TTY          TIME CMD
      1 ?        00:00:01 systemd
...
```

Просто посмотреть в директории процесса **/proc/1**:

```console
vagrant@vagrant:~$ cat /proc/1/status
Name:	systemd
Umask:	0000
State:	S (sleeping)
...
```

### 4. Как будет выглядеть команда, которая перенаправит вывод stderr ls на другую сессию терминала?

Терминал 1:

```commandline
vagrant@vagrant:~$ tty
/dev/pts/0
vagrant@vagrant:~$ ls UNEXISTING_REPOSITORY 2> /dev/pts/1
```

Терминал 2:

```commandline
vagrant@vagrant:~$ tty
/dev/pts/1
vagrant@vagrant:~$ ls: cannot access 'UNEXISTING_REPOSITORY': No such file or directory
```

### 5. Получится ли одновременно передать команде файл на stdin и вывести ее stdout в другой файл? Приведите работающий пример.

```commandline
vagrant@vagrant:~$ echo "test" > input.txt
vagrant@vagrant:~$ ls
input.txt
vagrant@vagrant:~$ cat < input.txt > output.txt
vagrant@vagrant:~$ cat output.txt
test
vagrant@vagrant:~$
```


### 6. Получится ли находясь в графическом режиме, вывести данные из PTY в какой-либо из эмуляторов TTY? Сможете ли вы наблюдать выводимые данные?

Ну устный ответ: да. В графическом режиме у нас так же выделяется PTY и можно перенаправить вывод из одного терминала в другой.

Возможно я что-то путаю. Но в целом здесь есть рабочий пример того как это сделать: https://dev.to/napicella/comment/np73 


> На лекции говорили что GUI не нужен будет для решения домашних заданий, у меня сейчас 
убунту без графического режима.

К сожалению, у меня сейчас нет возможности развернуть стенд с GUI Linux.

Недопонимание какое-то странное возникает: Александр Крылов на лекции сказал что GUI вообще не понадобятся.

https://netology.ru/profile/program/devsys-12/lessons/100767/lesson_items/501756 - посмотрите, пожалуйста, 
ответ Александра на мой вопрос в конце лекции. Чтобы не искать, вот таймкод 1:06:35

Я работал несколько лет на Linux(в качестве основно рабочей машины с GUI) в далеких 2010-2012 годах, мне они не нравятся, в отличие от работы с Linux по SSH.

### 7. Выполните команду bash 5>&1. К чему она приведет? Что будет, если вы выполните echo netology > /proc/$$/fd/5? Почему так происходит?
Открывается новая сессия терминала и создается файловый дескриптор 5.

```commandline
vagrant@vagrant:~$ ls -l /proc/$$/fd/
total 0
lrwx------ 1 vagrant vagrant 64 Sep 22 17:00 0 -> /dev/pts/0
lrwx------ 1 vagrant vagrant 64 Sep 22 17:00 1 -> /dev/pts/0
lrwx------ 1 vagrant vagrant 64 Sep 22 17:00 2 -> /dev/pts/0
lrwx------ 1 vagrant vagrant 64 Sep 22 17:00 255 -> /dev/pts/0
lrwx------ 1 vagrant vagrant 64 Sep 22 17:00 5 -> /dev/pts/0
vagrant@vagrant:~$
```

### 8. Получится ли в качестве входного потока для pipe использовать только stderr команды, не потеряв при этом отображение stdout на pty? Напоминаем: по умолчанию через pipe передается только stdout команды слева от | на stdin команды справа. Это можно сделать, поменяв стандартные потоки местами через промежуточный новый дескриптор, который вы научились создавать в предыдущем вопросе.

Да, благодаря статье https://catonmat.net/bash-one-liners-explained-part-three кажется понял как это работает.

Вот пример в pipe отображает только stderr от команды слева, но при этом мы не видим stdout от команды слева.

```commandline
vagrant@vagrant:~$ ls UNEXISTING_FOLDER | 3>&1 1>&2 2>&3
ls: cannot access 'UNEXISTING_FOLDER': No such file or directory
vagrant@vagrant:~$ ls /var/tmp/ | 3>&1 1>&2 2>&3
vagrant@vagrant:~$ ls /var/tmp/
systemd-private-65ddbae72f0e409abf5d99a0e4e56275-systemd-logind.service-WobFWi
systemd-private-65ddbae72f0e409abf5d99a0e4e56275-systemd-resolved.service-yFUQBg
vagrant@vagrant:~$
```

### 9. Что выведет команда cat /proc/$$/environ? Как еще можно получить аналогичный по содержанию вывод?

Текущий ENV.

Можно так:
```commandline
vagrant@vagrant:~$ printenv
SHELL=/bin/bash
LANGUAGE=en_US:
PWD=/home/vagrant
...
```

Можно так:
```commandline
vagrant@vagrant:~$ env
SHELL=/bin/bash
LANGUAGE=en_US:
PWD=/home/vagrant
...
```

### 10. Используя man, опишите что доступно по адресам /proc/<PID>/cmdline, /proc/<PID>/exe.

```commandline
/proc/[pid]/cmdline
  This read-only file holds the complete command line for the process,  un‐
  less  the  process  is a zombie.  In the latter case, there is nothing in
  this file: that is, a read on this file will return  0  characters.   The
  command-line  arguments appear in this file as a set of strings separated
  by null bytes ('\0'), with a further null byte after the last string.
```

### 11. Узнайте, какую наиболее старшую версию набора инструкций SSE поддерживает ваш процессор с помощью /proc/cpuinfo.

Командой:
```commandline
vagrant@vagrant:~$ cat /proc/cpuinfo | grep flags
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx rdrand hypervisor lahf_lm abm 3dnowprefetch invpcid_single pti fsgsbase avx2 invpcid rdseed clflushopt md_clear flush_l1d arch_capabilities
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx rdrand hypervisor lahf_lm abm 3dnowprefetch invpcid_single pti fsgsbase avx2 invpcid rdseed clflushopt md_clear flush_l1d arch_capabilities
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx rdrand hypervisor lahf_lm abm 3dnowprefetch invpcid_single pti fsgsbase avx2 invpcid rdseed clflushopt md_clear flush_l1d arch_capabilities
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx rdrand hypervisor lahf_lm abm 3dnowprefetch invpcid_single pti fsgsbase avx2 invpcid rdseed clflushopt md_clear flush_l1d arch_capabilities
```

Для каждого ядра выдаст список поддерживаемых им инструкций.

Ответ: **sse**, **sse2**

### 12. При открытии нового окна терминала и vagrant ssh создается новая сессия и выделяется pty. Это можно подтвердить командой tty, которая упоминалась в лекции 3.2. Однако:

Ссылка на видео с примером подключения по ssh к **localhost**:
https://disk.yandex.ru/i/VwI64qxRvTRYUg

```commandline
-t   Force pseudo-terminal allocation.  This can be used to execute arbitrary screen-based programs on a remote machine, which
     can be very useful, e.g. when implementing menu services.  Multiple -t options force tty allocation, even if ssh has no lo‐
     cal tty.
```


### 13. Бывает, что есть необходимость переместить запущенный процесс из одной сессии в другую. Попробуйте сделать это, воспользовавшись reptyr. Например, так можно перенести в screen процесс, который вы запустили по ошибке в обычной SSH-сессии.

> Пробовал, все зависало на смерть на Ubuntu 20.04 TLS.

Сейчас разобрался, проблема в целом возникла из-за того что на MacOS у меня неправильно передавались 
коды клавиш в терминал. 
Специально для того чтобы **reptyr** протестировать поднял инстанс Ubuntu на Amazon.

Ссылка на видео с примером использования утилиты:
https://disk.yandex.com/i/p2rZTQzUNVvfMQ

P.S.: у меня проблемы со screen и tmux утилитами, клавиатура MacOS по дефолту не дружит с ними. 
Поэтому пример перехвата процесса сделан на команде **top**.

### 14. sudo echo string > /root/new_file не даст выполнить перенаправление под обычным пользователем, так как перенаправлением занимается процесс shell'а, который запущен без sudo под вашим пользователем. Для решения данной проблемы можно использовать конструкцию echo string | sudo tee /root/new_file. Узнайте что делает команда tee и почему в отличие от sudo echo команда с sudo tee будет работать.

Команда **tee** перенаправляет данные из входного потока в выходной или файлы.

```commandline
vagrant@vagrant:~$ man tee
tee - read from standard input and write to standard output and files
```

Первый вариант не работает из-за того что bash запущен не под рутом, а sudo для echo не работает из-за того что это 
shell builtin команда, а tee сама по себе и ее уровень доступа можно расширить через **sudo**.

```commandline
vagrant@vagrant:~$ type echo
echo is a shell builtin
```

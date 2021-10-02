# 3.3. Операционные системы, лекция 1

### 1. Какой системный вызов делает команда cd? Вам нужно найти тот единственный вывод strace, который относится именно к cd.

```commandline
vagrant@vagrant:~$ strace /bin/bash -c 'cd /tmp' 2>&1
execve("/bin/bash", ["/bin/bash", "-c", "cd /tmp"], 0x7ffcffb4dd90 /* 27 vars */) = 0
brk(NULL)                               = 0x55dacaff4000
... ... ...
rt_sigprocmask(SIG_BLOCK, NULL, [], 8)  = 0
stat("/tmp", {st_mode=S_IFDIR|S_ISVTX|0777, st_size=4096, ...}) = 0
chdir("/tmp")                           = 0
rt_sigprocmask(SIG_BLOCK, [CHLD], [], 8) = 0
rt_sigprocmask(SIG_SETMASK, [], NULL, 8) = 0
exit_group(0)                           = ?
+++ exited with 0 +++
```

Ответ: **chdir("/tmp")**

### 2. Попробуйте использовать команду file на объекты разных типов на файловой системе. Например:

```commandline
vagrant@netology1:~$ file /dev/tty
/dev/tty: character special (5/0)
vagrant@netology1:~$ file /dev/sda
/dev/sda: block special (8/0)
vagrant@netology1:~$ file /bin/bash
/bin/bash: ELF 64-bit LSB shared object, x86-64
```

Используя strace выясните, где находится база данных file на основании которой она делает свои догадки.

```commandline
vagrant@vagrant:~$ strace /bin/bash -c 'file /dev/tty'
execve("/bin/bash", ["/bin/bash", "-c", "file /dev/tty"], 0x7ffe3b41b800 /* 27 vars */) = 0
...
openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3
...
+++ exited with 0 +++
```

Ответ: **/usr/share/misc/magic.mgc**

### 3. Предложите способ обнуления открытого удаленного файла (чтобы освободить место на файловой системе).

> Предположим, приложение пишет лог в текстовый файл. Этот файл оказался удален (deleted в lsof), 
> однако возможности сигналом сказать приложению переоткрыть файлы или просто перезапустить приложение – нет.
> Так как приложение продолжает писать в удаленный файл, место на диске постепенно заканчивается.
> Основываясь на знаниях о перенаправлении потоков предложите способ обнуления открытого удаленного файла
> (чтобы освободить место на файловой системе).

Для этого нужно знать PID процесса, который пишет в файл.
Правило хорошего тона при написании демонов создавать pid-файлы(.pid) при запуске.

При удалении исходного файла и отсутствии возможности перезапустить или пересоздать файл,
мы можем обнулить поток перенаправив на него **/dev/null**.

```commandline
vagrant@vagrant:~$ cat /proc/5408/fd/3 > /tmp/test2
```

### 4. Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?

Нет.
Процесс при завершении (как нормальном, так и в результате не обрабатываемого сигнала) освобождает все свои ресурсы и становится «зомби».
Процесс становится пустой записью в таблице процессов, хранящей статус завершения, предназначенный для чтения родительским процессом.

Источник: https://ru.wikipedia.org/wiki/Процесс-зомби 

### 5. В iovisor BCC есть утилита opensnoop:

```commandline
root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop
/usr/sbin/opensnoop-bpfcc
```

На какие файлы вы увидели вызовы группы open за первую секунду работы утилиты? 
Воспользуйтесь пакетом bpfcc-tools для Ubuntu 20.04.

Вот список файлов(syscall open()) которые выдал трейс opensnoop-bpfcc в первые секунды работы:  

```commandline
root@vagrant:/home/vagrant# /usr/sbin/opensnoop-bpfcc
PID    COMM               FD ERR PATH
619    irqbalance          6   0 /proc/interrupts
619    irqbalance          6   0 /proc/stat
619    irqbalance          6   0 /proc/irq/20/smp_affinity
619    irqbalance          6   0 /proc/irq/0/smp_affinity
619    irqbalance          6   0 /proc/irq/1/smp_affinity
619    irqbalance          6   0 /proc/irq/8/smp_affinity
619    irqbalance          6   0 /proc/irq/12/smp_affinity
619    irqbalance          6   0 /proc/irq/14/smp_affinity
619    irqbalance          6   0 /proc/irq/15/smp_affinity
808    vminfo              4   0 /var/run/utmp
604    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
604    dbus-daemon        18   0 /usr/share/dbus-1/system-services
604    dbus-daemon        -1   2 /lib/dbus-1/system-services
604    dbus-daemon        18   0 /var/lib/snapd/dbus-1/system-services/
808    vminfo              4   0 /var/run/utmp
604    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
604    dbus-daemon        18   0 /usr/share/dbus-1/system-services
604    dbus-daemon        -1   2 /lib/dbus-1/system-services
604    dbus-daemon        18   0 /var/lib/snapd/dbus-1/system-services/
619    irqbalance          6   0 /proc/interrupts
619    irqbalance          6   0 /proc/stat
619    irqbalance          6   0 /proc/irq/20/smp_affinity
619    irqbalance          6   0 /proc/irq/0/smp_affinity
619    irqbalance          6   0 /proc/irq/1/smp_affinity
619    irqbalance          6   0 /proc/irq/8/smp_affinity
619    irqbalance          6   0 /proc/irq/12/smp_affinity
619    irqbalance          6   0 /proc/irq/14/smp_affinity
619    irqbalance          6   0 /proc/irq/15/smp_affinity
808    vminfo              4   0 /var/run/utmp
604    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
604    dbus-daemon        18   0 /usr/share/dbus-1/system-services
604    dbus-daemon        -1   2 /lib/dbus-1/system-services
604    dbus-daemon        18   0 /var/lib/snapd/dbus-1/system-services/
808    vminfo              4   0 /var/run/utmp
604    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
604    dbus-daemon        18   0 /usr/share/dbus-1/system-services
```

А что именно требовалось в этом задании, кроме установки iovisor BCC? 
Просто узнать что с помощью этой утилиты можно удобным способом отлаживать системный вызов open()?

### 6. Какой системный вызов использует uname -a? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в /proc, где можно узнать версию ядра и релиз ОС.

```commandline
vagrant@vagrant:~$ strace uname -a
execve("/usr/bin/uname", ["uname", "-a"], 0x7ffdc32f9c08 /* 27 vars */) = 0
...
uname({sysname="Linux", nodename="vagrant", ...}) = 0
fstat(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(0x88, 0), ...}) = 0
uname({sysname="Linux", nodename="vagrant", ...}) = 0
uname({sysname="Linux", nodename="vagrant", ...}) = 0
write(1, "Linux vagrant 5.4.0-80-generic #"..., 105Linux vagrant 5.4.0-80-generic #90-Ubuntu SMP Fri Jul 9 22:49:44 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
) = 105
close(1)                                = 0
close(2)                                = 0
exit_group(0)                           = ?
+++ exited with 0 +++
```

Ответ: Системный вызов uname

Ответ 2: man-источник по системному вызову https://man7.org/linux/man-pages/man2/uname.2.html

```
Part of the utsname information is also accessible via
/proc/sys/kernel/{ostype, hostname, osrelease, version,
domainname}.
```

### 7. Чем отличается последовательность команд через ; и через && в bash? Например:

```commandline
root@netology1:~# test -d /tmp/some_dir; echo Hi
Hi
root@netology1:~# test -d /tmp/some_dir && echo Hi
root@netology1:~#
```

**;** - это как команда в новой строке, которая игнорирует все что было до нее и ответы предыдущих команд.

**&&** - это логическое И. Команда выполниться только если статус код предыдущей команды был 0.

**set -e** - в bash-скрипте указывает скрипту чтобы он завершился, если одна из команд вернула ненулевой ответ.

```commandline
-e  Exit immediately if a command exits with a non-zero status.
```

Есть ли смысл использовать в bash &&, если применить set -e?

Ответ: кажется что - **нет**. 

Интересны подводные камни, может что-то упускаю, по факту, скрипт будет выполняться до тех пор, пока exit-код всех команд 0.

Тестовый скрипт такой был:

```commandline
vagrant@vagrant:~$ cat script.sh
#!/bin/bash
set -e
test -d /var
echo "/var exist"
test -d /tmp/some_dir
echo "/tmp/some_dir exist"
```

### 8. Из каких опций состоит режим bash set -euxo pipefail и почему его хорошо было бы использовать в сценариях?

Вырезал вывода всех этих опций из **set --help**

```commandline
vagrant@vagrant:~$ set --help
      -e  Exit immediately if a command exits with a non-zero status.
      -u  Treat unset variables as an error when substituting.
      -x  Print commands and their arguments as they are executed.
      -o option-name
          Set the variable corresponding to option-name:
          pipefail      the return value of a pipeline is the status of
                        the last command to exit with a non-zero status,
                        or zero if no command exited with a non-zero status
```

**-u** - указывает что при подстановке переменных, которые не установлены или удалены скрипту нужно падать с ошибкой

**-x** - указывает скрипты выводить в stdout команды, которые будут выполнены, до их исполнения.

**-o pipefail** - по умолчанию, если какая-то команда внутри pipe вернет ненулевой ответ скрипт проигнорирует
эту ошибку и продолжит свое выполнение. С этой опцией статус команд pipe будут аффектить работу скрипта,
который их вызывал.

#### Почему его хорошо было бы использовать в сценариях?

Ответ: потому что без этого bash-скрипты(в особенности большие) могут отрабатывать не так как положено и возвращать статус код 0(успех).

С такими скриптами очень сложно будет построить надежную автоматизацию. 

Лучше если он будет падать сразу и об этом будет известно в моменте.

### 9. Используя -o stat для ps, определите, какой наиболее часто встречающийся статус у процессов в системе. В man ps ознакомьтесь (/PROCESS STATE CODES) что значат дополнительные к основной заглавной буквы статуса процессов. Его можно не учитывать при расчете (считать S, Ss или Ssl равнозначными).

```commandline
vagrant@vagrant:~$ ps -o pid,user,comm,etime,%mem,%cpu,stat
PID  USER     COMMAND             ELAPSED %MEM %CPU STAT
3833 vagrant  bash               06:48:11  0.4  0.0 Ss
3876 vagrant  man                06:40:55  0.3  0.0 T
3886 vagrant  pager              06:40:55  0.2  0.0 T
3900 vagrant  man                06:39:24  0.3  0.0 T
3910 vagrant  pager              06:39:23  0.3  0.0 T
4443 vagrant  ps                    00:00  0.3  0.0 R+
```

**S** - interruptible sleep (waiting for an event to complete)
**T** - stopped by job control signal
**R** - running or runnable (on run queue)

**s** - is a session leader
**+** - is in the foreground process group


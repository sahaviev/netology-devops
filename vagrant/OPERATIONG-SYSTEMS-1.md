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


### 4. Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?

Нет.

### 6. Какой системный вызов использует uname -a? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в /proc, где можно узнать версию ядра и релиз ОС.

### 7. Чем отличается последовательность команд через ; и через && в bash? Например:


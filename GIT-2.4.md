# 2.4. Инструменты Git

### 1. Найдите полный хеш и комментарий коммита, хеш которого начинается на `aefea`.

Команда поиска коммита `git show aefea -q`. Вывод команды:
```commandline
commit aefead2207ef7e2aa5dc81a34aedf0cad4c32545
Author: Alisdair McDiarmid <alisdair@users.noreply.github.com>
Date:   Thu Jun 18 10:29:58 2020 -0400

    Update CHANGELOG.md
```

>  Я специально сделал **git show** с ключом **-q**, чтобы убрать ненужный output. 

Полный хеш: **aefead2207ef7e2aa5dc81a34aedf0cad4c32545**

Комментарий: *Update CHANGELOG.md*

### 2. Какому тегу соответствует коммит `85024d3`?

Команда поиска коммита `git show 85024d3 -q`. Вывод команды:

```commandline
commit 85024d3100126de36331c6982bfaac02cdab9e76 (tag: v0.12.23)
Author: tf-release-bot <terraform@hashicorp.com>
Date:   Thu Mar 5 20:56:10 2020 +0000

    v0.12.23
```

Тэг: **tag: v0.12.23**

### 3. Сколько родителей у коммита `b8d720`? Напишите их хеши.

Это мерж коммит. 

Это можно понять посмотрев команду `git show b8d720`:

```
commit b8d720f8340221f2146e4e4870bf2ee0bc48f2d5
Merge: 56cd7859e 9ea88f22f
Author: Chris Griggs <cgriggs@hashicorp.com>
Date:   Tue Jan 21 17:45:48 2020 -0800

    Merge pull request #23916 from hashicorp/cgriggs01-stable

    [Cherrypick] community links
```

Проверить родителей можно так: 

`git show b8d720^1` - commit **56cd7859e05c36c06b56d013b55a252d0bb7e158**

`git show b8d720^2` - commit **9ea88f22fc6269854151c571162c5bcf958bee2b**


### 4. Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами v0.12.23 и v0.12.24.


Команда `git log v0.12.23..v0.12.24 --oneline`

```commandline
33ff1c03b (tag: v0.12.24) v0.12.24
b14b74c49 [Website] vmc provider links
3f235065b Update CHANGELOG.md
6ae64e247 registry: Fix panic when server is unreachable
5c619ca1b website: Remove links to the getting started guide's old location
06275647e Update CHANGELOG.md
d5f9411f5 command: Fix bug when using terraform login on Windows
4b6d06cc5 Update CHANGELOG.md
dd01a3507 Update CHANGELOG.md
225466bc3 Cleanup after v0.12.23 release
```

### 5. Найдите коммит в котором была создана функция `func providerSource`, ее определение в коде выглядит так `func providerSource(...)` (вместо троеточего перечислены аргументы).

Ответ: **8c928e83589d90a031f811fae52a81be7153e82f**

Команда для поиска всех коммитов с выхождением функции:

`git log -S'func providerSource' --oneline`

Результат будет в хронологическом порядке, соответственно, 
самый нижний коммит скорее всего тот самый где функцию создали.

```commandline
5af1e6234 main: Honor explicit provider_installation CLI config when present
8c928e835 main: Consult local directories as potential mirrors of providers
```

### 6. Найдите все коммиты в которых была изменена функция `globalPluginDirs`.

Команда для поиска файлов где используется строка:

`git grep globalPluginDirs`

В выдаче по ключевому слову func понимаем что тело функции описана в файле **plugins.go**:

```commandline
commands.go:            GlobalPluginDirs: globalPluginDirs(),
commands.go:    helperPlugins := pluginDiscovery.FindPlugins("credentials", globalPluginDirs())
internal/command/cliconfig/config_unix.go:              // FIXME: homeDir gets called from globalPluginDirs during init, before
plugins.go:// globalPluginDirs returns directories that should be searched for
plugins.go:func globalPluginDirs() []string {
```

Команда для поиска всех коммитов где функцию изменяли:

`git log -L :globalPluginDirs:plugins.go --oneline -q`

Выдача:

```commandline
78b122055 Remove config.go and update things using its aliases
52dbf9483 keep .terraform.d/plugins for discovery
41ab0aef7 Add missing OS_ARCH dir to global plugin paths
66ebff90c move some more plugin search path logic to command
8364383c3 Push plugin discovery down into command package
```

Нам тело не нужно, поэтому с флагами **--oneline** и **-q**.

### 7. Кто автор функции `synchronizedWriters`?

Команда для поиска всех коммитов с выхождением функции:

`git log -S'synchronizedWriters'`

Ее выдача:
```commandline
commit bdfea50cc85161dea41be0fe3381fd98731ff786
Author: James Bardin <j.bardin@gmail.com>
Date:   Mon Nov 30 18:02:04 2020 -0500

    remove unused

commit fd4f7eb0b935e5a838810564fd549afe710ae19a
Author: James Bardin <j.bardin@gmail.com>
Date:   Wed Oct 21 13:06:23 2020 -0400

    remove prefixed io

    The main process is now handling what output to print, so it doesn't do
    any good to try and run it through prefixedio, which is only adding
    extra coordination to echo the same data.

commit 5ac311e2a91e381e2f52234668b49ba670aa0fe5
Author: Martin Atkins <mart@degeneration.co.uk>
Date:   Wed May 3 16:25:41 2017 -0700

    main: synchronize writes to VT100-faker on Windows

    We use a third-party library "colorable" to translate VT100 color
    sequences into Windows console attribute-setting calls when Terraform is
    running on Windows.

    colorable is not concurrency-safe for multiple writes to the same console,
    because it writes to the console one character at a time and so two
    concurrent writers get their characters interleaved, creating unreadable
    garble.

    Here we wrap around it a synchronization mechanism to ensure that there
    can be only one Write call outstanding across both stderr and stdout,
    mimicking the usual behavior we expect (when stderr/stdout are a normal
    file handle) of each Write being completed atomically.
```

`git show 5ac311e2` покажет выхождения тела функции и то что функция была
создана именно в этом коммите. 

Ответ: **Author: Martin Atkins**
# Comment extraire le message caché du signal final

En supposant que le micro puisse capter et transmettre les ultra sons. Comment l'encoder et le décoder ?

Nous pouvons assigner une fréquence à chaque charactères du message.
(ex. 'a'=20kHz, 'b'=20.1kHz, 'c'=...)

Nous pouvons réaliser un programme sur la tablette afin de lire le message et le convertir en un série de signaux.

De l'autre coté du système d'audio conférence. Nous pouvons placer un filtre passe-haut afin d'isoler les notre message [20-22.6]kHz suivi d'un appareil qui interprètera ces fréquences sous la formes de charactères.

Dans le cas ou nous ne pouvons pas utiliser une plage aussi grande. Il serait possible de transmettre les charactères sous la forme d'un nombre dans un base $n$.

- Si nous avons une plage très courte : binaire ($n=2$)
- Si nous avons une plage un peut plus grande : trinaire ($n=3$)
- ...

Si le signal est trop long, nous pouvons assigner assigner les codes les plus courts aux lettre les plus fréquentes. et nous pouvons réserver un signal particulier pour signaler la fin du charactère actuel.

Par exemple, les lettres 'a' et 'e' sont très communes. Nous pouvons ainsi assigner le signal $0$ pour la lettre 'a' et $1$ pour la lettre 'e'.
Nous pouvons prendre $0$=>20kHz, $1$=>20.1kHz et $EOC$=>20.2kHz
Étant donné que nous devrons transmettre en série. Nous pouvons également utiliser un blanc comme signal. Dans se cas, il faut transmettre des la fréquence de l'orloge 

Dans ce cas, le signal final sera
$$
[0, EOC, 1, EOC]
$$
ou $EOC$ signifit 'End Of Character'

Au lieux de transmettre 16 signaux (si nous résevons un octes pour chaques charactères) nous en transmitons que 4.

Et un charactère plus rare, disons 'z' aura un code plus long, (ex. 'z'=$1011$)

De l'autre côté du système d'audio conférence. Il n'aura qu'a lire le signal en sortie de filtre et changer de charactère à chaque fois qu'il recois le signal $EOC$


Voici une potentielle séquence de transmition

Début du signal
- EOC
- EOC

Qualibration (fréquences et horloge)
- 0
- 1
- 0
- 1
- 0
- 1

La séquence de qualibration peut être répété plusieurs fois pour s'assurer que le récepteur soit bien qualibré.

Fin de la séquence de qualibration
- EOC
- EOC

Début de la transmition
- 1
- 1
- EOC
- 1
- 0
- 1
- EOC

Fin de la transmition
- EOC
- EOC
- EOC
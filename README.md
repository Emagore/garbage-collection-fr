[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
[![Garbage-Collection](https://img.shields.io/github/v/release/bruxy70/Garbage-Collection.svg)](https://github.com/bruxy70/Garbage-Collection)
![Maintenance](https://img.shields.io/maintenance/yes/2026.svg)

# ♻️ Garbage Collection (fork FR)

Cette intégration Home Assistant permet de créer des capteurs personnalisés pour gérer les calendriers de collecte des déchets.

---

## 🍴 Fork personnel

Ce dépôt est un **fork personnel** de :
https://github.com/bruxy70/Garbage-Collection

L’intégration originale n’est plus activement maintenue depuis fin 2022.

---

## ✨ Modifications apportées dans ce fork

### 🇫🇷 Gestion intégrée des jours fériés

Ajout d’une fonctionnalité native permettant de décaler automatiquement les collectes si un jour férié est détecté dans la semaine.

- Utilise la librairie Python `holidays`
- Aucun blueprint externe requis
- Fonctionne avec un code pays (par défaut : FR)
- Analyse la semaine ISO complète
- Décale la collecte d’un jour si nécessaire (avec propagation si jours fériés consécutifs)

---

## ⚠️ Compatibilité Home Assistant

Compatible Home Assistant récent (2024+ / 2026)

Corrections incluses :
- remplacement de `async_forward_entry_setup` (obsolète)
- utilisation de `async_forward_entry_setups`
- support du reload dynamique des options

---

## 📦 Installation

### Installation manuelle

1. Copier le dossier :
2. 
2. Redémarrer Home Assistant
3. Ajouter l’intégration via l’interface

---

### Installation via HACS

1. Ajouter ce dépôt dans HACS (Custom repository)
2. Installer “Garbage Collection”
3. Redémarrer Home Assistant
4. Configurer via l’interface

---

## ⚙️ Configuration

Configuration via :
Paramètres → Appareils et services → Ajouter un assistant (Helper)

---

## 🧩 Fonctionnalités

- 📅 Hebdomadaire
- 🔁 Toutes les X semaines
- 📆 Tous les X jours
- 🗓️ Mensuel (n-ième semaine ou jour du mois)
- 🎂 Annuel
- 🔗 Groupement de capteurs
- ✋ Mode manuel avancé

---

## 🧪 États du capteur

| État | Signification |
|------|--------------|
| 0 | Collecte aujourd’hui |
| 1 | Collecte demain |
| 2 | Collecte plus tard |

---

## 📊 Attributs

- `next_date` → prochaine collecte
- `days` → jours restants
- `last_collection` → dernière collecte

---

## 🛠️ Services

- `garbage_collection.collect_garbage`
- `garbage_collection.update_state`
- `garbage_collection.add_date`
- `garbage_collection.remove_date`
- `garbage_collection.offset_date`

---

## 🧠 Mode avancé

Permet des règles personnalisées via automations Home Assistant.

⚠️ réservé aux utilisateurs avancés

---

## 📅 Jours fériés

- détection automatique
- décalage des collectes
- configuration par pays (`holiday_country`)

---

## ❤️ Remarque

Ce fork est personnel et expérimental.
Il peut diverger du projet original.

---

## 📜 Licence

Basé sur le projet original de bruxy70.
Même licence que l’original.
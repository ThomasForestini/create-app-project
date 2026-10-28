# Plan — Phase 2 : QCM photo

> PRD parent : `PRD.md`
> Date : 2026-10-28

## Architecture retenue

- `[DEV] odoo-qcm` : lit l'image, puis appelle `odoo-question` en mode `qcm`.
  - Lecture par Sonnet 5.5 en sortie structurée `{lisible, question, choix[], plusieurs_reponses}`.
  - Si l'image est illisible, il demande une nouvelle photo sans appeler `odoo-question`.
  - Deux déclencheurs : Execute Workflow Trigger (appel par Telegram) et webhook protégé Header Auth (`POST {image_base64}`, utilisé par le banc).
- `odoo-question` en mode `qcm` : il reçoit les choix et renvoie en plus `bonnes_reponses` (lettres), `explication` et `ecart_version`.
  - Recherche, rédaction et contrôle en ligne de la Phase 1 réutilisés tels quels.
  - Le mode texte ne change pas.
- Source des questions : `~/Downloads/Odoo 19 certification.pdf` (mail de Rémy Claes, 28 pages, questions v19).
  - Les surlignages de Rémy (vert = ses réponses, orange = erreurs probables, bleu = réponse alternative) sont gardés comme simples métadonnées.
  - Ils ne servent jamais de corrigé et ne sont jamais montrés au modèle.
- Les vraies photos viennent d'un support sans surlignage. Les images du banc sont rendues en texte neutre.

## Tâches

- [ ] **1. Extraction du pool + échantillon de 30.** Fait quand :
  - `docs/evaluation/qcm/pool.json` contient toutes les questions du PDF : texte, choix, module, couleur de Rémy en métadonnée.
  - 30 questions sont marquées `echantillon`, sur au moins 6 modules, dont toutes les questions orange et bleu.
  - Le nombre de questions est contrôlé à la main sur 3 pages du PDF.
- [ ] **2. Corrigé pré-rempli puis validé par Thomas** (après 1). Fait quand :
  - `docs/evaluation/qcm/corrige.json` donne pour chacune des 30 questions : la ou les bonnes réponses, une URL de la doc v20, la méthode (doc / runbot) et un indicateur `ecart_v19_v20`.
  - Une grille de relecture est générée.
  - Les 30 questions ont `valide: true` après la relecture de Thomas.
- [ ] **3. Images du banc** (après 1). Fait quand :
  - 30 PNG neutres (texte noir sur fond blanc, aucun surlignage) sont dans `docs/evaluation/qcm/img/Q01..Q30.png`.
  - 5 vraies photos de téléphone sont dans `docs/evaluation/qcm/img/photo-01..05.jpg`, dont une floue ou de biais.
  - 3 images sont contrôlées visuellement.
- [ ] **4. Mode `qcm` dans `odoo-question`.** Fait quand :
  - Un `curl` du webhook avec le texte et les choix de Q01 renvoie un JSON dont les `bonnes_reponses` font partie des choix, avec un `statut` et au moins une source v20.
  - D001 en mode texte donne le même format qu'avant (non-régression).
  - L'export `workflows/odoo-question.workflow.json` est à jour.
- [ ] **5. Workflow `[DEV] odoo-qcm`** (après 4). Fait quand :
  - `curl` avec Q01.png renvoie la question lue, les choix et la réponse.
  - Une image blanche ou très floue renvoie `lisible: false` sans appeler `odoo-question`.
  - Sans jeton, la réponse est 403.
  - Le workflow est exporté dans `workflows/odoo-qcm.workflow.json`.
- [ ] **6. Photo dans `telegram-assistant`** (après 5).
  - Le filtre accepte texte et photo.
  - Le workflow aiguille selon le type et télécharge la photo en meilleure résolution.
  - Le message affiche la question lue, la ou les réponses, l'explication, la source et l'écart v19/v20 éventuel.

  Fait quand :
  - Une photo envoyée depuis le téléphone reçoit sa réponse en moins de 60 s.
  - Une question texte marche toujours.
  - Les deux exports sont à jour.
- [ ] **7. Script `scripts/banc-qcm.py`** (après 2, 3, 5).
  - Il rejoue les images sur le webhook et compare au corrigé.
  - Il écrit `docs/evaluation/{date}-qcm.json` et un résumé : taux de bonnes réponses, nombre de « Documenté » faux, lecture correcte, latence et coût moyens.
  - L'URL et le jeton du webhook sont lus depuis `.env`.

  Fait quand :
  - Une passe de 5 images produit le JSON et le résumé.
  - Le jeton apparaît 0 fois dans le code (`grep`).
- [ ] **8. Passe complète + rapport** (après 7). Les 35 images sont rejouées. Fait quand :
  - `docs/evaluation/{date}-qcm.md` compare les mesures aux critères du PRD.
  - Chaque erreur est classée : lecture, recherche, raisonnement ou écart de version.
  - Des pistes sont notées si le taux est sous 90 %.
  - La case « Banc de mesure rejouable » est cochée dans le PRD.

## Critère de phase complète

- [ ] Tâches 1 à 8 cochées
- [ ] Depuis Telegram, une photo de QCM reçoit la question lue, la bonne réponse, une explication et une source v20 ; une photo illisible déclenche la demande d'une nouvelle photo
- [ ] Taux de bonnes réponses mesuré sur 30 questions, avec un corrigé validé à la main
  - Objectifs du PRD : ≥ 90 %, ≤ 1 « Documenté » faux, < 60 s, ≤ 0,05 USD.
  - Décision du 28/10/2026 : la phase peut être close sous ces objectifs. Le rapport donne alors les pistes, et l'amélioration passe en Phase 4 ou dans une phase dédiée.

## Prochaine étape

`/execute docs/plans/phase-2-plan.md`

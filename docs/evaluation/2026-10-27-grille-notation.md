# Grille de notation — duel 27/10/2026

Pour chaque question, note **A** et **B** : `Complète`, `Partielle` ou `Incorrecte` (définitions sous chaque question).
Remplace `___` par ta note. Les modèles sont masqués : la clé est dans `*-grille-cle.json`, à ouvrir après.

| Question | A | B |
|---|---|---|
| Q1 | ___ | ___ |
| Q2 | ___ | ___ |
| Q3 | ___ | ___ |
| Q4 | ___ | ___ |
| Q5 | ___ | ___ |
| Q6 | ___ | ___ |
| Q7 | ___ | ___ |
| Q8 | ___ | ___ |
| Q9 | ___ | ___ |
| Q10 | ___ | ___ |
| Q11 | ___ | ___ |
| Q12 | ___ | ___ |

---

## Q1 — 20.0 — CRM → Ventes → Stock → Facturation → Paiement

> Un client accepte un devis issu d'une opportunité CRM pour des produits stockés, facturés à la livraison. Quelles sont toutes les étapes dans Odoo 20, de l'opportunité jusqu'au paiement enregistré, et quelles configurations faut-il faire au préalable ?

**Indispensable** : Préalables : produit « Goods » avec « Track Inventory » ; politique de facturation « Delivered quantities ». Flux : « New Quotation » depuis l'opportunité → lignes, envoi → confirmation (commande) → opportunité « Won » → livraison validée (quantités livrées) → « Create Invoice » → facture confirmée → paiement enregistré (« Register Payment ») → rapprochement.

**Erreurs à éviter** : « Produit stockable » ; facturer avant la livraison alors que la politique est « livrée » ; affirmer que l'opportunité passe à « Won » toute seule sans source.

**Complète** : Les 2 préalables et toutes les étapes, sources 20.0. · **Partielle** : Flux juste, mais un préalable ou l'étape paiement manque (résultat I4-7 : installation des modules, bouton CRM → devis, validation facture/paiement manquants). · **Incorrecte** : Politique de facturation inversée, ordre faux, ou source d'une autre version non signalée.

### Réponse A

**Statut : À vérifier** · couverture partial

✅ Le processus démarre dans l'application **CRM** avec la conversion d'une piste en opportunité (dans **CRM app ‣ My Pipeline**) d'où un devis peut être créé. Une fois le devis renseigné (avec le client et le produit stockable dont la politique de facturation est sur **Delivered quantities**) et confirmé en bon de commande (**Sales Order**), un bon de livraison est généré automatiquement. Il faut alors valider la livraison via le bouton intelligent **Delivery** avant de pouvoir générer et confirmer la facture (**Create Invoice**), puis enregistrer le paiement du client.

_Prérequis_
- ✅ L'application **Inventory** doit être installée pour pouvoir traiter les bons de livraison.
- ✅ Sur la fiche du produit, la politique de facturation (invoicing policy) doit être configurée sur **Delivered quantities** (quantités livrées), et le produit doit être un produit stockable (storable **Product**) et non un produit de type **Service** ou abonnement.
- ✅ Optionnel : pour envoyer automatiquement un e-mail de confirmation lorsque la livraison est terminée (statut **Done**), allez dans **Inventory ‣ Configuration ‣ Settings**, faites défiler jusqu'à la section **Shipping** et activez **Confirmation Email**.
- ✅ Optionnel (Comptabilité) : configurer des comptes d'attente (outstanding accounts) ou définir le compte bancaire principal comme compte d'attente sur le mode de paiement du journal bancaire si l'on souhaite que l'enregistrement du paiement réduise immédiatement le montant dû (**Amount Due**) ou passe directement la facture au statut **Paid** sans rapprochement bancaire.

_Étapes_
1. ✅ **Convertir la piste en opportunité (si l'opportunité n'existe pas encore)** — Allez dans **CRM app ‣ Leads**, ouvrez la piste et cliquez sur **Convert to Opportunity** en haut à gauche. Dans la fenêtre, sélectionnez **Convert to opportunity** dans le champ **Conversion Action**, assignez éventuellement un **Salesperson** et une **Sales Team**, puis sous **Customer**, choisissez **Create a new customer** ou **Link to an existing customer**. Cliquez enfin sur **Create Opportunity**.
2. ⚠️ **Accéder à l'opportunité et créer le devis** — Rendez-vous dans **CRM app ‣ My Pipeline** pour voir l'opportunité et initier la création et l'envoi du devis depuis l'application *CRM* (ou depuis **Sales app** en cliquant sur **New** / **Create**).
3. ✅ **Renseigner et confirmer le devis en bon de commande** — Sur le formulaire de devis, sélectionnez le client dans le champ **Customer**. Sous l'onglet **Order Lines**, cliquez sur **Add a product** et sélectionnez le produit stockable. Une fois le client d'accord, cliquez sur **Confirm** : le statut passe à **Sales Order** et un bon de livraison est créé automatiquement.
4. ✅ **Traiter et valider le bon de livraison** — Depuis le bon de commande confirmé, cliquez sur le bouton intelligent **Delivery** en haut du formulaire pour ouvrir le bon de livraison. Une fois les opérations d'entrepôt et l'expédition réalisées, cliquez sur **Validate** sur le bon de livraison pour confirmer la livraison (au moins partielle).
5. ⚠️ **Créer et confirmer la facture client** — Revenez sur le bon de commande : le bouton **Create Invoice** est maintenant violet. Cliquez sur **Create Invoice**, sélectionnez le type de facture (par exemple **Regular Invoice** dans la fenêtre **Create invoices**), puis cliquez sur **Create Draft Invoice**. Sur le brouillon de facture (**Customer Invoice Draft**), cliquez sur **Confirm** pour valider la facture.
6. ✅ **Enregistrer le paiement sur la facture** — Sur la facture confirmée, cliquez sur **Pay** (ou **Register Payment**). Dans la fenêtre qui s'ouvre, sélectionnez le **Journal**, la **Payment Date** et vérifiez la **Payment Method** ainsi que le montant **Amount** (cliquez sur **full amount** si nécessaire) et le **Memo**. Cliquez sur **Create Payment** : la facture passe au statut **In payment** (ou directement **Paid** selon la configuration des comptes d'attente, sinon **Paid** après rapprochement bancaire).

_Attention_
- ✅ Lors de la conversion d'une piste en opportunité, tenter de convertir une piste ayant une probabilité de 100 % génère un message d'erreur.
- ✅ Avec la politique de facturation **Delivered quantities**, si un utilisateur tente de créer une facture avant d'avoir validé la quantité livrée, le système renvoie un message d'erreur.
- ✅ Aucun bon de livraison n'est généré pour les produits de type **Service** ou abonnement.
- ✅ Si aucun compte d'attente (outstanding account) n'est configuré lors de l'enregistrement du paiement, aucune écriture comptable n'est créée immédiatement, le montant dû (**Amount Due**) n'est pas mis à jour, et la facture ne passe au statut **Paid** qu'après le rapprochement avec une transaction bancaire.

_Pistes à tester_
- Piste à tester : Sur la fiche de l'opportunité dans **CRM app ‣ My Pipeline**, utiliser le bouton **New Quotation** en haut à gauche pour générer directement le devis pré-rempli avec le client lié à l'opportunité.
- Piste à tester : Lors de la confirmation du devis accepté par le client, faire passer l'opportunité CRM à l'étape gagnée (**Won**) depuis la fiche de l'opportunité.

_Non couvert_
- Le bouton exact permettant de générer le devis directement depuis la fiche de l'opportunité dans l'application CRM (le passage [8] mentionne que le processus est géré dans CRM mais n'en détaille pas les clics).
- Le chemin exact sur la fiche produit pour définir le type de produit sur stockable et la politique de facturation sur **Delivered quantities**.

_Sources :_ [1] applications/sales/sales/invoicing/invoicing_policy.html#invoice-ordered-quantity-workflow · [2] applications/sales/crm/acquire_leads/convert.html#convert-a-lead-into-an-opportunity · [3] applications/sales/sales/invoicing/invoicing_policy.html#invoice-what-is-delivered · [4] applications/websites/ecommerce/order_handling.html#delivery · [5] applications/sales/sales/invoicing/time_materials.html#invoice-purchase · [6] applications/finance/accounting/payments.html#registering-payments-from-an-invoice-or-bill · [7] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/delivery_three_steps.html#create-a-sales-order · [8] applications/sales/crm/acquire_leads/send_quotes.html · [9] applications/sales/sales/invoicing/invoicing_policy.html#invoice-delivered-quantity-workflow · [10] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_two_steps.html#create-sales-order

**Note A : ___**

### Réponse B

**Statut : À vérifier** · couverture partial

✅ Le flux documenté couvre : conversion du lead en opportunité (CRM), création du devis depuis le CRM (passage très succinct), confirmation en bon de commande, validation de la livraison, création de la facture (politique Delivered quantities), puis enregistrement du paiement via Pay. Les passages ne détaillent pas la création du devis depuis l'opportunité ni la configuration de la politique de facturation au niveau du produit (champ exact).

_Prérequis_
- ✅ Définir la politique de facturation du produit sur **Delivered quantities** dans la fiche produit.
- ✅ L'application Inventory doit être installée pour traiter les livraisons ; aucun bon de livraison n'est généré pour les produits **Service** ou d'abonnement.
- ⚠️ Optionnel : pour que le client paie en ligne, activer **Invoice Online Payment** dans **Accounting ‣ Configuration ‣ Settings**, section **Customer Payments**, puis **Save** ; vérifier que les payment providers sont bien configurés.
- ✅ Optionnel : pour envoyer un email de confirmation à la livraison, activer **Confirmation Email** dans **Inventory ‣ Configuration ‣ Settings**, section **Shipping**.

_Étapes_
1. ✅ **Ouvrir le lead** — Aller dans **CRM app ‣ Leads** et cliquer sur un lead pour l'ouvrir (si l'opportunité n'existe pas encore).
2. ✅ **Convertir en opportunité** — Cliquer sur **Convert to Opportunity**, choisir **Convert to opportunity** dans **Conversion Action**, puis éventuellement **Salesperson** et **Sales Team** (non obligatoires). Sous **Customer**, choisir **Create a new customer** ou **Link to an existing customer**, puis cliquer sur **Create Opportunity**. Un lead à 100 % de probabilité provoque une erreur.
3. ✅ **Retrouver l'opportunité** — Consulter l'opportunité créée dans **CRM app ‣ My Pipeline**.
4. ✅ **Créer et envoyer le devis** — Une fois le lead converti, l'étape suivante est de créer et d'envoyer un devis via l'application CRM (le détail des clics n'est pas donné dans les passages).
5. ⚠️ **Confirmer le devis** — Une fois le devis accepté, cliquer sur **Confirm** : il passe au stade **Sales Order**.
6. ✅ **Ouvrir le bon de livraison** — Après confirmation, un bon de livraison est créé automatiquement ; cliquer sur le smart button **Delivery** du bon de commande.
7. ✅ **Préparer et valider la livraison** — Effectuer les opérations d'entrepôt, puis cliquer sur **Validate** sur le bon de livraison une fois expédié. Au moins une livraison partielle validée est nécessaire pour facturer.
8. ⚠️ **Créer la facture** — Revenir au bon de commande : le bouton **Create Invoice** est devenu violet. Cliquer dessus, choisir le type de facture, cliquer sur **Create Draft Invoice**, puis confirmer la facture.
9. ✅ **Enregistrer le paiement** — Sur la facture, cliquer sur **Pay**, choisir **Journal** et **Payment Date**, vérifier **Payment Method**, **Amount** (ou **full amount**), éventuellement le **Memo**, puis cliquer sur **Create Payment**. La facture passe à **In payment**.
10. ⚠️ **Paiement en ligne (alternative)** — Si **Invoice Online Payment** est activé : cliquer sur **Send** sur la facture ; le client reçoit un lien vers son portail et clique sur **Pay Now** ; le paiement est enregistré et la facture passe à **In payment**.

_Attention_
- ✅ Créer une facture sans livraison validée renvoie un message d'erreur avec la politique **Delivered quantities**.
- ✅ Un lead à 100 % de probabilité ne peut pas être converti (erreur).
- ✅ Après l'enregistrement du paiement, la facture est **In payment** ; elle passe à **Paid** après rapprochement bancaire (avec comptes d'attente configurés ou non). Si le compte bancaire principal est défini comme compte d'attente du mode de paiement du journal, elle passe directement à **Paid**.
- ✅ Sans comptes d'attente (outstanding accounts), aucune écriture n'est créée et le **Amount Due** n'est pas mis à jour.
- ⚠️ Par défaut, seul Wire Transfer est activé comme payment provider, et ses détails doivent être saisis.

_Pistes à tester_
- Piste à tester : depuis l'opportunité, utiliser le bouton de création de devis (par ex. **New Quotation**) du CRM ; son libellé exact n'est pas confirmé par les passages.
- Piste à tester : si l'entrepôt est configuré en livraison en deux ou trois étapes, la livraison comportera plusieurs transferts (pick, pack, ship) à valider avant la facturation.

_Non couvert_
- Chemin exact de la fiche produit pour régler la politique de facturation (type de produit, champ Invoicing Policy).
- Détail de la création du devis depuis une opportunité CRM et de son envoi.
- Configuration du suivi de stock (produit storable) et des routes d'entrepôt.
- Configuration des journaux et comptes d'attente pour les paiements.

_Sources :_ [1] applications/sales/sales/invoicing/invoicing_policy.html#invoice-ordered-quantity-workflow · [2] applications/sales/crm/acquire_leads/convert.html#convert-a-lead-into-an-opportunity · [3] applications/sales/sales/invoicing/invoicing_policy.html#invoice-delivered-quantity-workflow · [4] applications/websites/ecommerce/order_handling.html#delivery · [5] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_two_steps.html#create-sales-order · [6] applications/finance/accounting/payments.html#registering-payments-from-an-invoice-or-bill · [8] applications/sales/crm/acquire_leads/send_quotes.html · [12] applications/finance/accounting/payments.html#online-payments

**Note B : ___**

---

## Q2 — 20.0 — Achats → Réception → Facture fournisseur → Paiement

> Comment configurer Odoo 20 pour qu'une facture fournisseur ne soit payée que pour les quantités réellement reçues ? Décris le flux complet : demande de prix, bon de commande, réception, facture et paiement.

**Indispensable** : « Control Policy » sur la **fiche produit** (onglet Purchase, section Vendor Bills) : « On received quantities » ; « 3-way matching » dans Achats → Configuration → Settings → section Invoicing ; champ « Should Be Paid » (onglet Other Info de la facture) ; « Billing Status » du bon de commande. Flux : RFQ → confirmation → réception validée → création de la facture depuis le bon de commande → facture confirmée → paiement.

**Erreurs à éviter** : Placer la politique de contrôle dans les paramètres généraux ; inventer un blocage du paiement au-delà de ce que décrit la doc pour « Should Be Paid ». Attention : la page elle-même est incohérente (défaut des biens écrit « On delivered quantities ») ; la réponse doit s'en tenir aux deux options de la case radio.

**Complète** : Politique produit, 3-way matching et flux complet, sources 20.0. · **Partielle** : Flux juste, mais politique ou 3-way matching absent. · **Incorrecte** : Politique « On ordered quantities » proposée pour ce besoin, réglage placé au mauvais endroit, ou réglage inventé.

### Réponse A

**Statut : À vérifier** · couverture complete

✅ Pour ne payer que les quantités reçues : définir la Control Policy du produit sur « On received quantities », activer le 3-way matching dans les réglages Purchase, puis suivre le flux RFQ, confirmation, réception (Validate), création de la facture depuis le PO, confirmation et paiement. La documentation ne détaille pas la création de la demande de prix au-delà du formulaire de base.

_Prérequis_
- ⚠️ Produit stockable (Goods) acheté auprès d'un fournisseur ; la politique de contrôle se règle sur la fiche produit.
- ✅ Le 3-way matching n'est prévu que pour fonctionner avec la politique de facturation (Bill Control) sur Received quantities.

_Étapes_
1. ✅ **Définir la politique de contrôle du produit** — Aller dans **Purchase app ‣ Products ‣ Products**, ouvrir le produit, onglet **Purchase**, section **Vendor Bills**, sous **Control Policy** cocher **On received quantities**, puis cliquer sur **Save**. La facture n'est alors créée qu'après réception d'une partie ou de la totalité de la commande, sur la base des quantités reçues.
2. ✅ **Activer le 3-way matching** — Aller dans **Purchase app ‣ Configuration ‣ Settings**, section **Invoicing**, cocher **3-way matching**, puis cliquer sur **Save**. Le champ **Should Be Paid** apparaît alors dans l'onglet **Other Info** des factures fournisseurs.
3. ✅ **Créer la demande de prix (RFQ)** — Aller dans **Purchase app ‣ New** pour ouvrir un formulaire RFQ vierge, sélectionner un **Vendor** et ajouter un **Product** stockable.
4. ✅ **Confirmer la commande** — Cliquer sur **Confirm Order**. Un bouton intelligent **Receipt** apparaît en haut à droite et ouvre la réception associée au bon de commande.
5. ✅ **Valider la réception** — Depuis le bouton **Receipt**, cliquer sur **Validate** : la réception passe à l'étape **Done**. Au retour sur le PO (fil d'Ariane), la colonne **Received** de la ligne produit reflète la quantité reçue.
6. ✅ **Créer la facture fournisseur depuis le PO** — Aller dans **Purchase app ‣ Orders ‣ Purchase Orders**, sélectionner le PO puis cliquer sur **Create Bill**. Une facture brouillon (**Draft**) s'ouvre. Si la quantité totale n'est pas reçue, seuls les produits reçus sont inclus.
7. ✅ **Contrôler le champ Should Be Paid** — Dans l'onglet **Other Info**, vérifier **Should Be Paid** (options : **Yes**, **No**, **Exception**). Il vaut **Yes** à la création ; si le brouillon est modifié (quantités, prix, produits ajoutés), il passe à **Exception**, sans blocage ni message d'erreur.
8. ✅ **Confirmer la facture** — Sélectionner une date dans **Bill Date**, puis cliquer sur **Confirm**.
9. ✅ **Enregistrer le paiement** — Cliquer sur **Register Payment** (ou **Pay**), vérifier les informations préremplies (**Journal**, **Payment Method**, **Amount**, **Currency**), puis cliquer sur **Create Payment**. Un montant inférieur au solde restant produit un paiement partiel.
10. ✅ **Vérifier le statut final** — Une fois la facture marquée **Paid** (bannière verte), **Should Be Paid** passe automatiquement à **No**. Selon la configuration des comptes de paiement en attente, la facture peut d'abord être **In payment** jusqu'au rapprochement bancaire.

_Attention_
- ✅ Le PO sélectionné ne doit pas déjà être facturé, sinon une fenêtre **Invalid Operation** s'affiche.
- ✅ Le statut **Should Be Paid** est défini automatiquement mais peut être modifié manuellement via la liste déroulante de l'onglet **Other Info**.
- ✅ Les passages indiquent que la politique par défaut des biens (Goods) diffère de « On received quantities » selon le type de produit (libellé « On delivered quantities » dans le passage) : vérifier explicitement la politique de chaque produit.
- ⚠️ Le champ **Should Be Paid** est un indicateur : Odoo ne bloque pas le paiement d'une facture en Exception.

_Non couvert_
- Détails de l'envoi de la RFQ au fournisseur et de son approbation (passages très généraux).
- Aucune information sur le nombre d'étapes de réception à configurer (1, 2 ou 3 étapes) pour ce besoin précis.

_Sources :_ [1] applications/inventory_and_mrp/purchase/manage_deals/control_bills.html#pay-vendor-bills-with-3-way-matching · [2] applications/inventory_and_mrp/purchase/manage_deals/control_bills.html#configuration · [3] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_three_steps.html#create-a-purchase-order · [4] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_two_steps.html#process-receipt · [5] applications/inventory_and_mrp/purchase/manage_deals/manage.html#bill-control-policies · [6] applications/finance/accounting/vendor_bills.html#payment-and-reconciliation · [7] applications/inventory_and_mrp/purchase/manage_deals/manage.html#way-matching · [8] applications/inventory_and_mrp/purchase/manage_deals/control_bills.html · [10] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_one_step.html#process-receipt · [12] applications/finance/accounting/payments.html#registering-payments-from-an-invoice-or-bill

**Note A : ___**

### Réponse B

**Statut : À vérifier** · couverture complete

⚠️ Pour garantir qu'une facture fournisseur ne soit facturée et payée que pour les quantités réellement reçues dans Odoo 20.0, il faut configurer la politique de contrôle de facturation (**Control Policy**) de l'article sur les quantités reçues (**On received quantities**) et activer la fonctionnalité de rapprochement tripartite (**3-way matching**). Le flux complet s'effectue ensuite de la demande de prix jusqu'à la réception en stock, la création de la facture sur base des quantités reçues, et l'enregistrement du paiement.

_Prérequis_
- ⚠️ Activer le rapprochement tripartite : allez dans **Purchase app ‣ Configuration ‣ Settings**, faites défiler jusqu'à la section **Invoicing**, cochez la case **3-way matching** et cliquez sur **Save**.
- ⚠️ Configurer la politique de contrôle sur l'article : allez dans **Purchase app ‣ Products ‣ Products**, ouvrez la fiche de l'article, allez dans l'onglet **Purchase**, section **Vendor Bills**, et sous **Control Policy**, sélectionnez **On received quantities** (qui est la politique par défaut pour les articles de type **Goods**), puis cliquez sur **Save**. La fonctionnalité **3-way matching** est uniquement conçue pour fonctionner avec cette politique.

_Étapes_
1. ✅ **Créer une demande de prix (RfQ) et confirmer le bon de commande (PO)** — Naviguez vers **Purchase app ‣ New** pour ouvrir un formulaire vierge de **Request for Quotation** (RfQ). Sélectionnez un fournisseur dans le champ **Vendor**. Sous l'onglet **Products**, cliquez sur **Add a product** pour ajouter votre article stockable, puis cliquez sur **Confirm Order**. La demande de prix passe alors à l'étape **Purchase Order** et un bouton intelligent **Receipt** apparaît en haut du formulaire.
2. ⚠️ **Réceptionner les articles en stock** — Cliquez sur le bouton intelligent **Receipt** en haut du bon de commande pour ouvrir le bon de réception d'entrepôt (**WH/IN**). Pour réceptionner les produits, cliquez sur **Validate** : la réception passe à l'étape **Done**. En revenant sur le bon de commande via le fil d'Ariane (breadcrumbs), la quantité dans la colonne **Received** sur la ligne d'article correspond désormais à la quantité commandée (**Quantity**).
3. ✅ **Générer la facture fournisseur (Vendor Bill)** — Allez dans **Purchase app ‣ Orders ‣ Purchase Orders**, sélectionnez le bon de commande souhaité et cliquez sur **Create Bill** (une facture ne peut être créée qu'une fois qu'au moins une partie des produits a été reçue, et Odoo n'inclut dans le brouillon que les quantités reçues). Cela ouvre un formulaire **Vendor Bill** à l'étape **Draft**. Dans l'onglet **Other Info**, le champ **Should Be Paid** est automatiquement défini sur **Yes**.
4. ✅ **Confirmer la facture fournisseur** — Sur la facture fournisseur en brouillon, sélectionnez une date dans le champ **Bill Date**, puis cliquez sur **Confirm**.
5. ⚠️ **Enregistrer le paiement** — Cliquez sur **Register Payment** (ou **Pay**). Dans la fenêtre qui s'ouvre, vérifiez ou sélectionnez les informations comptables (**Journal**, **Payment Date**, **Payment Method**, **Amount**, **Currency**, **Memo**), puis cliquez sur **Create Payment**. Une fois le paiement enregistré (et rapproché selon la configuration des comptes d'attente, affichant le bandeau vert **Paid** ou **In payment**), le statut du champ **Should Be Paid** dans l'onglet **Other Info** passe automatiquement à **No**.

_Attention_
- ✅ La fonctionnalité **3-way matching** est uniquement prévue pour fonctionner avec la politique de contrôle de facturation (**Bill Control** / **Control Policy**) configurée sur **Received quantities** (**On received quantities**).
- ✅ Lors de la création de la facture via **Create Bill**, le bon de commande sélectionné ne doit pas avoir déjà été facturé, sinon une fenêtre pop-up **Invalid Operation** apparaît.
- ✅ Si les informations de la facture en brouillon sont modifiées (par exemple, augmentation de la quantité facturée, changement du prix ou ajout d'articles), le champ **Should Be Paid** passe au statut **Exception**. Odoo signale ainsi l'écart mais ne bloque pas la modification et n'affiche pas de message d'erreur. Par ailleurs, le champ **Should Be Paid** peut toujours être modifié manuellement via son menu déroulant (**Yes**, **No**, **Exception**).
- ✅ Lors du paiement de la facture, le passage direct au statut **Paid** ou au statut **In payment** (nécessitant un rapprochement bancaire ultérieur) dépend de la configuration des comptes d'attente (outstanding accounts) sur le journal bancaire.

_Sources :_ [1] applications/inventory_and_mrp/purchase/manage_deals/control_bills.html#pay-vendor-bills-with-3-way-matching · [2] applications/inventory_and_mrp/purchase/manage_deals/control_bills.html#configuration · [3] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_three_steps.html#create-a-purchase-order · [5] applications/inventory_and_mrp/purchase/manage_deals/manage.html#bill-control-policies · [6] applications/finance/accounting/vendor_bills.html#payment-and-reconciliation · [7] applications/inventory_and_mrp/purchase/manage_deals/manage.html#way-matching · [8] applications/inventory_and_mrp/purchase/manage_deals/control_bills.html · [9] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_two_steps.html#create-purchase-order · [10] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_one_step.html#process-receipt · [12] applications/finance/accounting/payments.html#registering-payments-from-an-invoice-or-bill

**Note B : ___**

---

## Q3 — 19.0 — Valorisation permanente FIFO (anglo-saxonne)

> Pour un client en Odoo 19 en comptabilité anglo-saxonne, comment configurer la valorisation permanente des stocks en FIFO, et comment sont comptabilisés les mouvements de stock qui n'ont pas encore de facture ?

**Indispensable** : Comptabilité → Configuration → Settings → section Inventory Valuation, **au niveau de la société** : « Perpetual (at invoicing) », « Inventory Cost Method » = FIFO, « Valuation Account », « Variation Account » (type actif courant ou charge, avec l'effet de chaque choix), journal, « Periodic Valuation » (Manual / Daily / Monthly) ; surcharge possible sur la catégorie de produits ; comptes « Inventory Loss » et « Production » sur les emplacements. Mouvements non facturés : écriture de clôture de stock (stock closing entry), le compte de variation sert de tampon jusqu'aux écritures de régularisation (accrual entries).

**Erreurs à éviter** : **Procédure Odoo 18** : catégorie de produits → « Inventory Valuation » = « Automated », comptes « Stock Input / Stock Output ». Ce n'est plus le modèle de 19 (même page en 20). Dire que la valorisation comptable suit chaque mouvement en temps réel.

**Complète** : Réglages société + compte de variation + écriture de clôture, sources 19.0 ; mention éventuelle de la procédure 18 uniquement comme différence signalée. · **Partielle** : Réglages justes mais clôture / compte de variation absents. · **Incorrecte** : Procédure 18 présentée comme valable en 19.

### Réponse A

**Statut : À vérifier** · couverture partial

⚠️ Pour configurer la valorisation permanente en FIFO, le paramétrage s'effectue au niveau de la société dans les paramètres de la comptabilité (**Perpetual (at invoicing)** et **First in First Out (FIFO)**), et peut être surchargé sur la catégorie de produit. Concernant la comptabilisation, depuis Odoo 19, la méthode permanente n'enregistre plus d'écritures comptables à chaque mouvement de stock et les comptes d'entrée/sortie de stock (stock input/output) ne sont plus utilisés. La valorisation de stock est impactée au niveau de la facture, tandis que les mouvements de stock n'ayant pas encore de facture (factures fournisseurs à recevoir, factures clients à émettre et autres écarts entre la valeur de stock et la comptabilité) sont gérés via une écriture de clôture (closing entry).

_Prérequis_
- ⚠️ Utiliser le standard comptable **Anglo-Saxon**, dans lequel le coût des marchandises vendues (COGS) est reconnu en charge lorsque la facture client est comptabilisée.
- ⚠️ En cas de mise à niveau vers Odoo 19, vérifier au préalable les commandes d'achat ou de vente reçues/livrées non encore liées à des factures, comptabiliser les factures brouillon existantes, et transférer les soldes non nuls des comptes **Stock Interim** vers le compte de valorisation des stocks par pièce comptable (une action serveur permet d'identifier et d'appliquer automatiquement ce changement après la migration).

_Étapes_
1. ✅ **Configurer la méthode de valorisation et de coût au niveau de la société** — Allez dans **Accounting ‣ Configuration ‣ Settings**, puis faites défiler jusqu'à la section **Inventory Valuation**. Définissez **Inventory Valuation** sur **Perpetual (at invoicing)** et **Inventory Cost Method** sur **First in First Out (FIFO)**. Si nécessaire, vous pouvez automatiser le processus d'écriture de clôture (**Periodic Valuation**) en choisissant **Manual**, **Daily** ou **Monthly**.
2. ✅ **Définir les comptes et le journal de valorisation** — Toujours dans **Accounting ‣ Configuration ‣ Settings** sous **Inventory Valuation**, définissez le **Valuation Account** (compte d'actif pour la valeur financière du stock), cliquez sur le lien interne **(internal link)** à côté pour ouvrir le compte **Stock Valuation** et mettre à jour le **Variation Account**. Sélectionnez également le **Journal** dans lequel comptabiliser les écritures de valorisation, et cliquez sur **locations** si vous devez définir les comptes sur les emplacements dédiés (**Inventory Loss** ou **Production**).
3. ✅ **Configurer ou surcharger la catégorie de produits (optionnel)** — Les comptes par défaut, méthodes de valorisation et méthodes de coût peuvent être surchargés sur la catégorie de produits. Allez dans **Inventory app ‣ Configuration ‣ Categories**, ouvrez ou créez une catégorie, définissez **Costing Method** sur **First In First Out (FIFO)** et **Inventory Valuation** sur **Perpetual (at invoicing)**. Assurez-vous également que les comptes requis sont définis sur la catégorie/le produit (notamment le compte de stock et le compte **Expense** / **Cost of Goods Sold**).
4. ⚠️ **Activer la stratégie d'enlèvement FIFO sur la catégorie (si souhaité)** — Pour forcer la stratégie d'enlèvement physique en FIFO, allez dans **Inventory app ‣ Configuration ‣ Categories**, sélectionnez la catégorie de produits et définissez le champ **Force Removal Strategy** sur **First In First Out (FIFO)**.
5. ⚠️ **Comptabiliser les factures et l'écriture de clôture pour les mouvements sans facture** — En méthode **Perpetual** anglo-saxonne depuis Odoo 19, les factures fournisseurs (**BILL**) débitent le compte **Stock** et créditent **Payable**, tandis que les factures clients (**INVOICE**) comptabilisent le **COGS** et le **Stock** en plus de **Income** et **Receivable**. Pour les mouvements de stock non encore facturés (**Bills to receive**, **Invoices to issue**, ainsi que les écarts entre valorisation de stock et valorisation comptable), ils sont pris en compte via l'écriture de clôture (**Closing**) entre le compte **Stock** et le compte **Variation**.

_Attention_
- ✅ Votre question porte sur Odoo 19 alors que les passages fournis sont issus de la documentation d'Odoo 20.0 ; toutefois, les passages mentionnent explicitement les changements introduits à partir d'Odoo 19.
- ✅ Changement majeur depuis Odoo 19 : avant Odoo 19, la méthode **Perpetual** générait des écritures comptables en temps réel à chaque mouvement de stock. Depuis Odoo 19, les comptes d'entrée/sortie de stock (stock input/output) ne sont plus utilisés : la méthode **Perpetual** impacte le compte de valorisation au niveau de la facture, complétée par une écriture de clôture.
- ✅ Incohérence documentaire dans les passages fournis : certains passages (comme les exemples sur les retours de marchandises ou le paramétrage des rebuts) décrivent encore l'ancien fonctionnement avec génération d'écritures en temps réel à la réception/livraison via le compte **Stock Input** (`Stock Interim (Received)`), ce qui contredit les passages dédiés aux nouveautés d'Odoo 19.
- ⚠️ Lorsqu'une stratégie d'enlèvement est définie à la fois sur l'emplacement et sur la catégorie de produit via le champ **Force Removal Strategy**, c'est la valeur de la catégorie de produit qui est prioritaire.
- ✅ Les structures de comptes et les scénarios de valorisation variant selon les entreprises, il est recommandé de valider ces étapes avec un comptable ou un expert en valorisation des stocks Odoo.

_Pistes à tester_
- Piste à tester : Vérifier dans le menu de comptabilité où se génère et se consulte l'écriture de clôture (closing entry) permettant de comptabiliser les factures à recevoir (Bills to receive) et les factures à émettre (Invoices to issue), et tester l'option d'automatisation (Manual, Daily, Monthly) vue dans les paramètres.

_Non couvert_
- La procédure détaillée et le chemin de menu exact pour générer, consulter ou valider l'écriture de clôture (closing entry) qui régularise les réceptions non facturées (Bills to receive) et les livraisons non facturées (Invoices to issue) ne sont pas décrits dans les extraits fournis.
- Le détail précis des lignes d'écritures comptables spécifiques aux comptes de régularisation (Bills to receive / Invoices to issue) lors de la clôture n'est pas documenté dans les passages.

_Sources :_ [1] applications/finance/accounting/get_started/inventory_valuation.html#upgrade-process-for-anglo-saxon-perpetual · [2] applications/finance/accounting/get_started/inventory_valuation.html#configuration · [3] applications/inventory_and_mrp/inventory/inventory_valuation/scrapped_inventory_valuation.html#configure-the-product-category · [4] applications/finance/accounting/get_started/avg_price_valuation.html#on-product-delivery · [5] applications/finance/accounting/get_started/avg_price_valuation.html#summary · [6] applications/finance/accounting/get_started/inventory_valuation.html#accounting-standards · [7] applications/inventory_and_mrp/inventory/inventory_valuation/cheat_sheet.html#changes-in-odoo-19 · [8] applications/inventory_and_mrp/inventory/inventory_valuation/cheat_sheet.html#accounting-methods · [9] applications/inventory_and_mrp/inventory/shipping_receiving/removal_strategies/fifo.html#on-the-product-category · [11] applications/finance/accounting/get_started/avg_price_valuation.html#in-odoo

**Note A : ___**

### Réponse B

**Statut : À vérifier** · couverture partial

✅ La question vise Odoo 19, alors que les passages décrivent Odoo 20. La valorisation permanente se règle au niveau société dans **Accounting ‣ Configuration ‣ Settings** (section **Inventory Valuation**) : méthode **Perpetual (at invoicing)**, méthode de coût **First in First Out (FIFO)**, compte de valorisation, **Journal**. Ces valeurs peuvent être surchargées sur la catégorie de produits. Pour les mouvements sans facture, le **Variation account** sert de compte tampon jusqu'à l'enregistrement des écritures de régularisation. Depuis Odoo 19, la méthode permanente impacte le compte de valorisation au niveau de la facture, avec une écriture de clôture pour les écarts.

_Prérequis_
- ⚠️ Accès aux réglages de **Accounting** et aux catégories de produits de l'application **Inventory**.
- ⚠️ Dans la pratique anglo-saxonne, prévoir les comptes suivants : **Stock Account** sur la catégorie de produits, **Stock Variation** sur le compte de stock, compte de charge/**Cost of Goods Sold** sur le produit ou la catégorie, et optionnellement **Inventory Adjustment** sur l'emplacement **Inventory Loss**.

_Étapes_
1. ✅ **Ouvrir les réglages de valorisation** — Aller dans **Accounting ‣ Configuration ‣ Settings**, puis dans la section **Inventory Valuation**.
2. ✅ **Choisir la valorisation permanente** — Dans **Inventory Valuation**, choisir **Perpetual (at invoicing)** (l'autre option étant **Periodic (at closing)**). Ce réglage est de niveau société.
3. ✅ **Choisir FIFO au niveau société** — Dans **Inventory Cost Method**, choisir **First in First Out (FIFO)** (les autres options sont **Standard Price** et **Average Cost (AVCO)**).
4. ✅ **Définir le compte de valorisation et le journal** — Renseigner le **Valuation Account** (compte d'actif représentant la valeur du stock physique) et le **Journal** où seront passées les écritures de valorisation. Cliquer sur la flèche à côté de **Valuation Account** pour ouvrir le compte **Stock Valuation** et mettre à jour le **Variation account**.
5. ✅ **Choisir le type du Variation account** — En anglo-saxon **Perpetual (at invoicing)**, le **Variation account** peut être un compte d'actif courant (suivi intermédiaire visible au bilan une fois l'écriture de clôture générée) ou un compte de charge (configuration plus simple, avec moins d'écritures intermédiaires).
6. ⚠️ **Surcharger sur la catégorie de produits si nécessaire** — Ouvrir **Inventory app ‣ Configuration ‣ Categories**, ouvrir ou créer une catégorie, régler **Costing Method** sur **First In First Out (FIFO)** et **Inventory Valuation** sur **Perpetual (at invoicing)**. Les comptes et méthodes par défaut peuvent être surchargés sur la fiche catégorie.
7. ✅ **Renseigner les comptes de la catégorie** — La fiche catégorie comporte aussi **Income Account**, **Expense Account**, **Stock Account** et **Price Difference Account** (ce dernier uniquement pour les catégories en **Perpetual (at invoicing)**).

_Attention_
- ✅ La question vise Odoo 19 alors que les passages décrivent Odoo 20 : la procédure peut différer dans cette version.
- ✅ Changement d'Odoo 19 : avant, la méthode permanente passait des écritures en temps réel à chaque mouvement de stock ; depuis Odoo 19, elle impacte le compte de valorisation au niveau de la facture, et l'écriture de clôture gère les factures à émettre, factures à recevoir, produits constatés d'avance, charges constatées d'avance et autres écarts.
- ⚠️ Depuis Odoo 19, les comptes stock input/output ne sont plus utilisés. Lors d'une migration, les soldes non nuls des comptes d'attente de stock doivent être transférés vers le compte de valorisation ; à faire avec un comptable ou un expert en valorisation.
- ✅ Pour les mouvements sans facture, le **Variation account** sert de compte tampon jusqu'à l'enregistrement des écritures de régularisation (accruals). Les variations liées aux réceptions et livraisons apparaissent dans la section **Stock Variation** du rapport Inventory Valuation.
- ✅ Les passages 5, 6 et 11 (comptes Stock Input / Stock Interim, exemple AVCO) décrivent un flux d'exemple en AVCO et ne sont pas utilisés ici comme règle générale pour FIFO.

_Pistes à tester_
- Piste à tester : sur une base de test, réceptionner un produit FIFO sans facture, puis consulter le rapport Inventory Valuation (section **Stock Variation**) et l'écriture de clôture pour vérifier les comptes mouvementés.

_Non couvert_
- Écritures comptables exactes générées pour une réception ou une livraison sans facture en FIFO, et méthode de déclenchement de l'écriture de clôture en perpétuel.
- Procédure détaillée pour Odoo 19 spécifiquement (les passages décrivent Odoo 20).

_Sources :_ [1] applications/finance/accounting/get_started/inventory_valuation.html#upgrade-process-for-anglo-saxon-perpetual · [2] applications/finance/accounting/get_started/inventory_valuation.html#configuration · [3] applications/inventory_and_mrp/inventory/inventory_valuation/scrapped_inventory_valuation.html#configure-the-product-category · [4] applications/finance/accounting/get_started.html#products-and-product-categories · [5] applications/finance/accounting/get_started/avg_price_valuation.html#in-odoo · [6] applications/finance/accounting/get_started/avg_price_valuation.html#on-product-delivery · [7] applications/inventory_and_mrp/inventory/inventory_valuation/cheat_sheet.html#changes-in-odoo-19 · [8] applications/inventory_and_mrp/inventory/inventory_valuation/cheat_sheet.html#accounting-methods · [10] applications/finance/accounting/get_started/inventory_valuation.html#variation-account · [11] applications/finance/accounting/get_started/avg_price_valuation.html#id1

**Note B : ___**

---

## Q4 — 18.0 — Frais d'approche (landed costs)

> En Odoo 18, comment répartir des frais de transport et de douane sur le coût des produits reçus d'un achat import, pour qu'ils soient intégrés à leur valorisation ?

**Indispensable** : Prérequis : catégorie de produits en **FIFO ou AVCO** (valorisation manuelle ou automatisée acceptée). Inventaire → Configuration → Settings → « Landed Costs » + journal par défaut. Produit de service avec « Is a Landed Cost » (onglet Purchase, section Vendor Bills) et « Default Split Method » (Equal, By Quantity, etc.). Flux : bon de commande → réception → facture fournisseur avec la ligne de frais → création du landed cost lié à la réception → validation → contrôle dans le rapport de valorisation et les écritures.

**Erreurs à éviter** : Exiger la valorisation automatisée (la page 18 accepte aussi le manuel) ; proposer le coût standard ; appliquer le modèle de valorisation de 19/20 (réglages au niveau société).

**Complète** : Prérequis FIFO/AVCO, réglage, produit de frais, flux et contrôle, sources 18.0. · **Partielle** : Flux juste sans le prérequis de méthode de coût, ou sans la méthode de répartition. · **Incorrecte** : Coût standard proposé, prérequis faux, ou procédure 19/20.

### Réponse A

**Statut : Non couvert** · couverture partial

⚠️ La fonction **Landed Costs** permet d'intégrer des frais supplémentaires (transport, assurance, droits de douane, taxes, etc.) dans la valorisation des produits. Il faut l'activer dans les réglages d'Inventory, puis créer un enregistrement de landed cost (depuis la facture fournisseur ou depuis **Inventory app ‣ Operations ‣ Landed Costs**), l'associer à un transfert validé, calculer la répartition et valider. Attention : les passages décrivent Odoo 20, la procédure peut différer en Odoo 18.

_Prérequis_
- ⚠️ Activer l'option **Landed Costs** dans **Inventory app ‣ Configuration ‣ Settings**, section **Valuation**, puis cliquer sur **Save**.
- ⚠️ Choisir un **Default Journal** (champ qui apparaît sous **Landed Costs** après l'enregistrement) pour comptabiliser les écritures liées aux landed costs.
- ⚠️ Le transfert (réception) concerné doit être validé : seuls les transferts validés peuvent être sélectionnés.

_Étapes_
1. ⚠️ **Activer la fonctionnalité Landed Costs** — Aller dans **Inventory app ‣ Configuration ‣ Settings**, section **Valuation**, cocher **Landed Costs** et cliquer sur **Save**.
2. ⚠️ **Définir le journal par défaut** — Une fois la page rafraîchie, sélectionner dans le champ **Default Journal** le journal où seront enregistrées toutes les écritures liées aux landed costs.
3. ⚠️ **Créer et valider la réception de l'achat** — Créer le bon de commande dans l'app **Purchase**, cliquer sur **Confirm Order**, puis utiliser le bouton intelligent **Receipt** pour ouvrir et valider la réception.
4. ⚠️ **Créer le landed cost** — Option 1 : cliquer sur **Create Landed Costs** en haut de la facture fournisseur (un enregistrement est créé avec un coût pré-rempli dans l'onglet **Additional Costs**). Option 2 : aller dans **Inventory app ‣ Operations ‣ Landed Costs** et cliquer sur **New**.
5. ⚠️ **Sélectionner le transfert** — Dans le formulaire **Landed Cost**, choisir dans la liste déroulante **Transfers** la réception concernée (transfert validé uniquement).
6. ⚠️ **Calculer la répartition** — Cliquer sur **Compute** (en bas du formulaire, sous le **Total:**).
7. ⚠️ **Vérifier l'impact sur la valorisation** — Ouvrir l'onglet **Valuation Adjustments** : **Original Value** (prix d'origine du PO), **Additional Landed Cost** (frais) et **New Value** (somme des deux, coût total du PO).
8. ⚠️ **Valider** — Cliquer sur **Validate** pour comptabiliser l'écriture du landed cost dans le journal.
9. ⚠️ **Contrôler l'écriture comptable** — Dans **Accounting app ‣ Accounting ‣ Journal Entries**, retrouver l'écriture par son numéro (ex. `STJ/2025/XXXXX`) et consulter les **Journal Items**.

_Attention_
- ⚠️ La question vise Odoo 18 : les passages décrivent Odoo 20.0, la procédure et les libellés peuvent différer en Odoo 18.
- ⚠️ Seuls les transferts validés peuvent être sélectionnés dans le champ **Transfers**.
- ⚠️ Les frais attachés à une réception augmentent la valeur des biens déjà reçus sans changer leur quantité.

_Pistes à tester_
- Piste à tester : pour séparer transport et douane, ajouter plusieurs lignes de coûts dans l'onglet **Additional Costs** du même landed cost (ou plusieurs landed costs), à vérifier dans votre version.
- Piste à tester : en Odoo 18, comparer les libellés et menus de la fonction Landed Costs avec la documentation 18.0, car ils peuvent différer.

_Non couvert_
- Les méthodes de répartition des frais (par quantité, poids, volume, valeur) ne sont pas décrites dans les passages.
- La procédure spécifique à Odoo 18 n'est pas couverte.
- Le paramétrage des produits de type frais (service/coût) et des comptes associés n'est pas détaillé.

_Sources :_ [1] applications/inventory_and_mrp/inventory/inventory_valuation/landed_costs.html · [2] applications/inventory_and_mrp/inventory/inventory_valuation/landed_costs.html#configuration · [3] applications/inventory_and_mrp/inventory/inventory_valuation/landed_costs.html#add-landed-cost · [6] applications/finance/fiscal_localizations/mexico.html#purchase-and-sales-flow · [8] applications/inventory_and_mrp/inventory/inventory_valuation/operations_valuation.html#receipts · [9] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_one_step.html#create-purchase-order

**Note A : ___**

### Réponse B

**Statut : À vérifier** · couverture partial

⚠️ Pour intégrer des frais supplémentaires tels que le transport, l'assurance ou les droits de douane dans la valorisation des produits reçus, il faut utiliser la fonctionnalité **Landed Costs** (coûts au débarquement). Après avoir activé cette option dans les paramètres de l'application **Inventory**, vous pouvez générer un enregistrement de coût au débarquement (depuis la facture fournisseur ou depuis le menu des opérations de stock), le lier au transfert de réception validé, calculer l'ajustement de valorisation, puis le valider pour comptabiliser l'écriture correspondante.

_Prérequis_
- ⚠️ La fonctionnalité **Landed Costs** doit être préalablement activée dans **Inventory app ‣ Configuration ‣ Settings** (section **Valuation**).
- ⚠️ Les méthodes de valorisation (**Perpetual (at invoicing)** ou **Periodic (at closing)**) et de coût (**Standard Price**, **First in First Out (FIFO)** ou **Average Cost (AVCO)**) se configurent au niveau de la société dans **Accounting ‣ Configuration ‣ Settings** (section **Inventory Valuation**), et peuvent être remplacées au niveau de la catégorie de produit.
- ⚠️ Le transfert (réception des marchandises) auquel les frais sont rattachés doit être validé : seuls les transferts validés peuvent être sélectionnés sur la fiche **Landed Cost**.

_Étapes_
1. ⚠️ **Activer la fonctionnalité Landed Costs** — Allez dans **Inventory app ‣ Configuration ‣ Settings**, faites défiler jusqu'à la section **Valuation**, cochez l'option **Landed Costs**, puis cliquez sur **Save**.
2. ⚠️ **Définir le journal comptable par défaut** — Une fois la page rafraîchie, dans le nouveau champ **Default Journal** situé sous **Landed Costs** (section **Valuation**), sélectionnez dans le menu déroulant le journal comptable dans lequel toutes les écritures liées aux coûts au débarquement doivent être enregistrées.
3. ⚠️ **Créer l'enregistrement de Landed Cost** — Depuis la facture fournisseur contenant les frais, cliquez sur **Create Landed Costs** en haut du formulaire (cela pré-remplit la ligne de produit dans l'onglet **Additional Costs**). Alternativement, allez dans **Inventory app ‣ Operations ‣ Landed Costs** et cliquez sur **New**.
4. ⚠️ **Rattacher la réception et calculer la répartition** — Sur le formulaire **Landed Cost**, cliquez sur le menu déroulant **Transfers** et sélectionnez le transfert validé concerné. Cliquez ensuite sur **Compute** (en bas du formulaire, sous le coût **Total:**).
5. ⚠️ **Vérifier l'ajustement et valider** — Consultez l'onglet **Valuation Adjustments** pour vérifier l'impact : **Original Value** (prix d'origine de la commande d'achat), **Additional Landed Cost** (coût additionnel) et **New Value** (somme des deux). Cliquez enfin sur **Validate** pour comptabiliser l'écriture de coût au débarquement dans le journal.
6. ⚠️ **Consulter l'écriture comptable (optionnel)** — Pour visualiser l'écriture générée, allez dans **Accounting app ‣ Accounting ‣ Journal Entries**, recherchez l'écriture par son numéro, puis ouvrez-la pour voir les **Journal Items**.

_Attention_
- ✅ Votre question porte sur Odoo 18, mais les passages fournis décrivent exclusivement Odoo 20.0. La procédure et les paramètres (notamment la configuration de la valorisation des stocks qui a évolué à partir d'Odoo 19) peuvent différer dans Odoo 18.

_Pistes à tester_
- Piste à tester : Configurer un produit de type service dédié aux frais de transport ou de douane en activant l'option permettant de le définir comme un coût au débarquement (Landed Cost) sur sa fiche produit, afin de faire apparaître le bouton **Create Landed Costs** sur la facture fournisseur.
- Piste à tester : Dans l'onglet **Additional Costs**, choisir la méthode de répartition souhaitée (par exemple par quantité, par coût actuel, par poids ou par volume) avant de cliquer sur **Compute**.
- Piste à tester : Vérifier que la catégorie des produits stockés reçus utilise bien une méthode de coût permettant la mise à jour de la valorisation (comme **FIFO** ou **AVCO** plutôt que **Standard Price**).

_Non couvert_
- Le paramétrage exact de la fiche produit correspondant aux frais de transport ou de douane pour qu'il soit reconnu comme un coût au débarquement.
- Les méthodes de répartition disponibles (quantité, poids, volume, coût, égal) dans l'onglet **Additional Costs** pour ventiler les frais entre les différents articles reçus.
- Les méthodes de coût (**Standard Price**, **FIFO**, **AVCO**) compatibles avec les **Landed Costs** dans un cas général (hors localisation mexicaine).

_Sources :_ [1] applications/inventory_and_mrp/inventory/inventory_valuation/landed_costs.html · [2] applications/inventory_and_mrp/inventory/inventory_valuation/landed_costs.html#configuration · [3] applications/finance/accounting/get_started/inventory_valuation.html#configuration · [4] applications/inventory_and_mrp/inventory/inventory_valuation/landed_costs.html#add-landed-cost · [12] applications/finance/accounting/get_started/inventory_valuation.html#option-1-server-action-journal-entry

**Note B : ___**

---

## Q5 — 20.0 — Entrepôt en 3 étapes

> Comment paramétrer un entrepôt Odoo 20 avec une réception en 3 étapes (quai, contrôle qualité, stock) et une livraison en 3 étapes (prélèvement, colisage, expédition) ? Quels réglages faire et quels transferts l'utilisateur doit-il traiter ?

**Indispensable** : Inventaire → Configuration → Settings → Warehouse → « Multi-Step Routes » (active aussi « Storage Locations ») ; sur l'entrepôt : réception en 3 étapes (input + quality + stock) et livraison en 3 étapes (pick + pack + ship). Transferts dans l'ordre : réception vers WH/Input → transfert vers WH/Quality Control → transfert vers WH/Stock ; prélèvement → colisage (WH/Packing Zone) → livraison depuis WH/Output, chacun validé.

**Erreurs à éviter** : Dire que l'application Qualité est nécessaire pour l'étape de contrôle (sans source) ; « produit stockable » ; ordre des transferts inversé.

**Complète** : Réglage, deux options d'entrepôt et les 6 transferts dans l'ordre. · **Partielle** : Réglages justes, transferts incomplets (ou l'inverse). · **Incorrecte** : Réglage manquant présenté comme facultatif, mauvaise option, ou application inventée comme prérequis.

### Réponse A

**Statut : À vérifier** · couverture partial

⚠️ Pour configurer un entrepôt avec des réceptions et des livraisons en 3 étapes dans Odoo 20.0, il faut activer la fonctionnalité **Multi-Step Routes** dans les paramètres de l'application **Inventory**, puis sélectionner les options à 3 étapes pour **Incoming Shipments** et **Outgoing Shipments** sur la fiche de l'entrepôt. Cela crée automatiquement les emplacements internes dédiés (**WH/Input**, **WH/Quality Control**, **WH/Packing Zone**, **WH/Output**). Les passages fournis détaillent entièrement le paramétrage et le flux conceptuel des emplacements, mais ne décrivent dans le détail opérationnel (boutons et écrans) que le transfert interne vers le contrôle qualité.

_Prérequis_
- ✅ Activer l'option **Multi-Step Routes** dans **Inventory app ‣ Configuration ‣ Settings** sous la section **Warehouse** (ce qui active également automatiquement la fonctionnalité **Storage Locations**).

_Étapes_
1. ✅ **Activer les routes en plusieurs étapes** — Allez dans **Inventory app ‣ Configuration ‣ Settings**. Sous la section **Warehouse**, cochez la case **Multi-Step Routes**, puis cliquez sur **Save**.
2. ✅ **Sélectionner l'entrepôt à configurer** — Naviguez vers **Inventory app ‣ Configuration ‣ Warehouses** et cliquez sur l'entrepôt souhaité pour ouvrir son formulaire détaillé.
3. ⚠️ **Configurer la réception en 3 étapes** — Sur le formulaire de l'entrepôt (sous l'onglet **Warehouse Configuration**), pour le champ **Incoming Shipments**, sélectionnez **Receive goods in input, then quality and then stock (3 steps)**. Cela crée deux nouveaux emplacements internes : *Input* (**WH/Input**) et *Quality Control* (**WH/Quality Control**).
4. ✅ **Configurer la livraison en 3 étapes** — Sur le même formulaire d'entrepôt, pour le champ **Outgoing Shipments**, sélectionnez **Pack goods, send goods in output and then deliver (3 steps)**. Cela crée deux nouveaux emplacements internes : *Packing Zone* (**WH/Packing Zone**) et *Output* (**WH/Output**).
5. ✅ **Renommer les emplacements créés (optionnel)** — Si vous souhaitez modifier le nom des emplacements générés automatiquement, allez dans **Inventory app ‣ Configuration ‣ Locations**, cliquez sur l'emplacement souhaité et mettez à jour le champ **Location Name**.
6. ⚠️ **Traiter les transferts de réception en 3 étapes** — Lors d'une réception en 3 étapes, les produits passent successivement par la zone d'entrée (**WH/Input**), la zone de contrôle qualité (**WH/Quality Control**), puis le stock : 
1. Validez d'abord la réception initiale.
2. Pour déplacer les produits vers le contrôle qualité, retournez sur le tableau de bord **Inventory Overview**, repérez la carte **Internal Transfers** et cliquez sur le bouton **# To Process**. Ouvrez le transfert associé à la réception validée et cliquez sur **Validate** pour transférer les produits de **WH/Input** vers **WH/Quality Control**.
3. Une fois l'inspection qualité réussie, les produits sont transférés de la zone qualité vers le stock.
7. ✅ **Traiter les transferts de livraison en 3 étapes** — Dans le processus par défaut de livraison en 3 étapes, l'utilisateur traite trois mouvements successifs : 
1. Les produits faisant partie de la commande de livraison sont prélevés dans l'entrepôt selon leur stratégie d'enlèvement et amenés vers la zone de colisage (**WH/Packing Zone**).
2. Après avoir été emballés dans la zone de colisage, les articles sont déplacés vers l'emplacement d'expédition (**WH/Output**).
3. Les produits sont enfin expédiés au client.

_Attention_
- ✅ Lors d'une réception en 3 étapes, les produits ne sont pas disponibles pour un traitement ultérieur tant qu'ils n'ont pas quitté la zone de contrôle qualité pour entrer en stock.
- ✅ L'activation de **Multi-Step Routes** active automatiquement l'option **Storage Locations**.
- ✅ Les réceptions et les livraisons n'ont pas l'obligation d'être configurées avec le même nombre d'étapes sur un entrepôt.

_Pistes à tester_
- Piste à tester : Sur le tableau de bord **Inventory Overview**, vérifier si des cartes d'opérations dédiées (par exemple pour le prélèvement *Pick*, le colisage *Pack*, le contrôle qualité ou le stockage) apparaissent ou si ces opérations sont regroupées sous **Internal Transfers** pour valider le transfert de **WH/Quality Control** vers **WH/Stock** ainsi que les étapes de livraison (**WH/Stock** -> **WH/Packing Zone** -> **WH/Output** -> Client).

_Non couvert_
- Les instructions pas-à-pas dans l'interface (noms exacts des cartes du tableau de bord et des boutons) pour valider la 1re étape de réception (vers **WH/Input**) et la 3e étape de réception (de **WH/Quality Control** vers le stock).
- Les instructions pas-à-pas dans l'interface (noms exacts des cartes d'opérations sur **Inventory Overview** et boutons à cliquer) pour traiter chacune des 3 étapes de livraison (Pick, Pack, Delivery).

_Sources :_ [1] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_three_steps.html#configuration · [2] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_two_steps.html#configuration · [3] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/delivery_three_steps.html#configuration · [5] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_three_steps.html#process-a-transfer-to-quality-control · [7] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_two_steps.html · [8] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_three_steps.html · [9] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/delivery_three_steps.html

**Note A : ___**

### Réponse B

**Statut : À vérifier** · couverture partial

✅ Il faut activer **Multi-Step Routes** dans les réglages d'Inventory, puis, dans la fiche de l'entrepôt, choisir **Receive goods in input, then quality and then stock (3 steps)** pour **Incoming Shipments** et **Pack goods, send goods in output and then deliver (3 steps)** pour **Outgoing Shipments**. Pour la réception, l'utilisateur valide la réception, puis le transfert interne vers le contrôle qualité. Pour la livraison, il traite le prélèvement, le colisage, puis la livraison (WH/OUT). Les passages ne détaillent pas tous les transferts (transfert final Quality Control → Stock, prélèvement et colisage).

_Prérequis_
- ✅ Activer l'option **Multi-Step Routes** dans **Inventory ‣ Configuration ‣ Settings ‣ Warehouse** ; cela active aussi **Storage Locations**.

_Étapes_
1. ✅ **Activer Multi-Step Routes** — Aller dans **Inventory ‣ Configuration ‣ Settings ‣ Warehouse**, cocher **Multi-Step Routes** et cliquer sur **Save**. **Storage Locations** est activé en même temps.
2. ✅ **Ouvrir l'entrepôt** — Aller dans **Inventory app ‣ Configuration ‣ Warehouses** et sélectionner l'entrepôt à modifier.
3. ✅ **Configurer la réception en 3 étapes** — Sur la fiche de l'entrepôt, sélectionner **Receive goods in input, then quality and then stock (3 steps)** pour **Incoming Shipments**.
4. ✅ **Configurer la livraison en 3 étapes** — Sur la même fiche, sélectionner **Pack goods, send goods in output and then deliver (3 steps)** pour **Outgoing Shipments**.
5. ✅ **Renommer les emplacements créés (optionnel)** — Les emplacements internes **WH/Input**, **WH/Quality Control**, **WH/Packing Zone** et **WH/Output** sont créés. Pour les renommer : **Inventory app ‣ Configuration ‣ Locations**, cliquer sur l'emplacement et modifier le nom.
6. ✅ **Traiter la réception (1/3)** — La réception (Vendors → WH/Input) est validée. Ce passage n'en détaille pas la procédure.
7. ✅ **Traiter le transfert vers le contrôle qualité (2/3)** — Cliquer sur **Inventory Overview** dans le fil d'Ariane, repérer la carte **Internal Transfers**, cliquer sur **# To Process**, choisir le transfert lié à la réception validée, puis cliquer sur **Validate** : le produit passe de **WH/Input** à **WH/Quality Control**.
8. ✅ **Transférer du contrôle qualité vers le stock (3/3)** — Un dernier transfert de stockage (**Storage**) déplace les produits de WH/Quality Control vers WH/Stock. Les produits ne sont pas disponibles tant qu'ils n'ont pas quitté la zone qualité pour le stock.
9. ✅ **Traiter la livraison** — Pour une commande client, le bouton **Delivery** affiche 3 transferts : prélèvement (picking), colisage (packing) et livraison. Ouvrir le transfert de livraison (WH/OUT) et cliquer sur **Validate** : le produit quitte **WH/Output** vers **Partners/Customers** et le statut passe à **Done**. Les transferts sont aussi accessibles via **Inventory app ‣ Operations ‣ Deliveries**.

_Attention_
- ✅ La réception et la livraison n'ont pas besoin d'avoir le même nombre d'étapes.
- ✅ Séparer prélèvement et colisage impose une validation à chaque étape ; si la même personne fait les deux, cela peut créer de la redondance et ralentir les opérations.
- ✅ Les contrôles qualité et le colisage ne nécessitent pas forcément un flux en 3 étapes (points de contrôle qualité activés séparément, contrôles manuels, fonction Packages).

_Non couvert_
- Procédure détaillée de validation de la réception (bon de commande) en 3 étapes.
- Procédure détaillée des transferts de prélèvement (pick) et de colisage (pack).
- Procédure détaillée du transfert final Quality Control → Stock.

_Sources :_ [1] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_three_steps.html#configuration · [2] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_two_steps.html#configuration · [3] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_three_steps.html · [4] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/delivery_three_steps.html#configuration · [6] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_three_steps.html#process-a-transfer-to-quality-control · [7] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_two_steps.html · [9] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/use_routes.html#incoming-shipments · [10] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations.html#three-step-flow · [11] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/delivery_three_steps.html#process-a-delivery

**Note B : ___**

---

## Q6 — 18.0 — Dropshipping

> En Odoo 18, comment vendre un produit livré directement par le fournisseur au client (dropshipping) : configuration, création automatique de l'achat, livraison, puis facturation client et fournisseur ?

**Indispensable** : Achats → Configuration → Settings → Logistics → « Dropshipping » ; produit « Can be Sold » et « Can be Purchased », fournisseur et prix dans l'onglet Purchase, route « Dropship » dans l'onglet Inventory. Flux : confirmation de la vente → demande de prix générée (bouton intelligent) → confirmation de l'achat → validation du transfert de dropship → facture client, facture fournisseur.

**Erreurs à éviter** : Exiger la route « Buy » en plus (la page dit qu'elle n'est pas nécessaire) ; dire que le stock de l'entrepôt est mouvementé ; inventer l'ordre de facturation si la doc ne le précise pas.

**Complète** : Configuration et flux complets ; facturation sourcée ou marquée « non vérifié ». · **Partielle** : Configuration et livraison justes, facturation absente ou non sourcée sans le dire. · **Incorrecte** : Route ou réglage faux, ou source 19/20 non signalée.

### Réponse A

**Statut : À vérifier** · couverture partial

⚠️ Les passages décrivent le dropshipping dans Odoo 20 (la question vise Odoo 18, la procédure peut différer) : activation de l'option Dropshipping, configuration du produit (vendeur, route Dropship), génération automatique d'une RFQ à la confirmation de la commande client, confirmation de l'achat, puis validation du bon de réception dropship. La facturation client et fournisseur spécifique au dropshipping n'est pas couverte par les passages.

_Prérequis_
- ⚠️ Application **Purchase** disponible (l'option **Dropshipping** se trouve dans ses réglages) et application **Sales** pour les commandes clients.
- ⚠️ Le produit doit avoir les cases **Can be Sold** et **Can be Purchased** activées, un vendeur et son prix dans l'onglet **Purchase**.

_Étapes_
1. ✅ **Activer le dropshipping** — Dans l'app **Purchase**, aller dans **Configuration ‣ Settings**, sous **Logistics** cocher **Dropshipping**, puis **Save**.
2. ✅ **Ouvrir la fiche produit** — Dans l'app **Sales**, aller dans **Products ‣ Products**, choisir un produit existant ou **Create**. Vérifier que **Can be Sold** et **Can be Purchased** sont cochés.
3. ✅ **Renseigner le fournisseur** — Dans l'onglet **Purchase**, indiquer le vendeur et le prix auquel il vend le produit. Plusieurs vendeurs possibles ; celui en haut de liste est sélectionné automatiquement pour les bons de commande.
4. ✅ **Activer la route Dropship** — Dans l'onglet **Inventory**, section **Routes**, cocher **Dropship**. Activer aussi **Buy** est optionnel : cela permet de choisir entre dropshipping et achat direct.
5. ⚠️ **Créer et confirmer la commande client** — Une fois la commande client créée pour le produit dropshippé, une RFQ est générée automatiquement. Les commandes se consultent dans **Sales ‣ Orders ‣ Orders** ; le smart button **Purchase** ouvre la RFQ associée.
6. ✅ **Confirmer la RFQ** — La confirmation de la RFQ la transforme en bon de commande et crée un reçu dropship lié. Il s'ouvre via le smart button **Dropship** du bon de commande.
7. ✅ **Valider la livraison** — Le reçu dropship affiche **Partners/Vendors** en **Source Location** et **Partners/Customers** en **Destination Location**. À la livraison au client, cliquer sur **Validate** pour confirmer la quantité livrée.
8. ✅ **Suivre les commandes dropship** — Dans le tableau de bord **Inventory** **Overview**, cliquer sur le bouton **# TO PROCESS** de la carte **Dropship**.

_Attention_
- ✅ La question vise Odoo 18 : les passages décrivent Odoo 20, la procédure peut différer dans cette version.
- ✅ Les produits dropshippés ne sont pas stockés : ils n'apparaissent pas dans les rapports *Locations* et *Aging Report*.

_Pistes à tester_
- Piste à tester : pour la facturation client, utiliser le bouton **Create Invoice** de la commande client (politique de facturation du produit), comme dans le flux standard de facturation.
- Piste à tester : pour la facturation fournisseur, créer la facture depuis le bon de commande confirmé (facture fournisseur) dans l'app Purchase.

_Non couvert_
- Procédure détaillée de facturation fournisseur pour un dropshipping non couverte par les passages.
- Facturation client spécifique au dropshipping (choix de la politique, moment de facturation) non documentée dans les passages.
- Différences de procédure entre Odoo 18 et Odoo 20 non documentées.

_Sources :_ [1] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/dropshipping.html#configure-products-to-be-dropshipped · [2] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/dropshipping.html#fulfill-orders-using-dropshipping · [6] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/dropshipping.html

**Note A : ___**

### Réponse B

**Statut : À vérifier** · couverture partial

✅ Le dropshipping (livraison directe par le fournisseur au client) s'effectue en activant la fonctionnalité **Dropshipping**, en configurant le produit avec un fournisseur et la route **Dropship**, puis en créant une commande client qui génère automatiquement une demande de prix (RfQ). Une fois l'achat confirmé, une réception de dropship est générée et doit être validée lors de la livraison au client. En revanche, les passages fournis ne détaillent pas les étapes de facturation client et fournisseur spécifiques à ce flux.

_Prérequis_
- ✅ Activer la fonctionnalité de dropshipping : aller dans l'application **Purchase** (ou **Inventory**), sélectionner **Configuration ‣ Settings**, puis sous la section **Logistics**, cocher la case **Dropshipping** et cliquer sur **Save**.
- ✅ Sur la fiche du produit concerné, s'assurer que les cases **Can be Sold** et **Can be Purchased** sont activées.

_Étapes_
1. ✅ **Configurer le fournisseur sur le produit** — Aller dans l'application **Sales**, cliquer sur **Products ‣ Products** et choisir un produit existant ou cliquer sur **Create**. Ouvrir l'onglet **Purchase** et spécifier un fournisseur ainsi que son prix de vente (si plusieurs fournisseurs sont ajoutés, celui en haut de la liste est sélectionné automatiquement pour les commandes d'achat).
2. ✅ **Activer la route Dropship sur le produit** — Sur la fiche du produit, sélectionner l'onglet **Inventory** et cocher la case **Dropship** dans la section **Routes** (ou **Operations**).
3. ⚠️ **Créer et confirmer la commande client (Sales Order)** — Aller dans **Sales app**, cliquer sur **New**, renseigner le client dans le champ **Customer**, ajouter le produit sous l'onglet **Product** via **Add a product**, puis cliquer sur **Confirm**.
4. ✅ **Accéder à la demande de prix (RfQ) générée automatiquement et la confirmer** — Depuis la commande client (accessible dans l'application **Sales** via **Orders ‣ Orders**), cliquer sur le smart button **Purchase** en haut du formulaire pour voir la demande de prix (RfQ) générée automatiquement. Confirmer cette demande de prix pour qu'elle devienne une commande d'achat (Purchase Order), ce qui crée et lie automatiquement un reçu de dropship.
5. ✅ **Valider la livraison directe au client (Dropship receipt)** — Ouvrir le reçu de dropship en cliquant sur le smart button **Dropship** en haut à droite de la commande d'achat (ou retrouver tous les ordres de dropship depuis le tableau de bord **Inventory** **Overview** en cliquant sur le bouton **# TO PROCESS** de la carte **Dropship**). Le document affiche **Partners/Vendors** dans **Source Location** et **Partners/Customers** dans **Destination Location**. Une fois le produit livré au client, cliquer sur le bouton **Validate** en haut à gauche pour confirmer la quantité livrée.

_Attention_
- ⚠️ Votre question porte sur Odoo 18 : les passages documentaires fournis décrivent exclusivement Odoo 20.0, la procédure ou certains libellés peuvent donc différer dans la version 18.
- ✅ Il n'est pas obligatoire d'activer la route **Buy** en plus de la route **Dropship**, mais activer les deux permet d'avoir l'option entre faire livrer le produit en dropshipping ou l'acheter directement.
- ✅ Comme les produits expédiés en dropshipping ne sont pas stockés dans l'inventaire de l'entreprise, ils n'apparaissent pas dans les rapports *Locations* et *Aging Report*.

_Pistes à tester_
- Piste à tester : Pour la facturation client, vérifier la politique de facturation (Invoicing Policy) sur la fiche produit (sur quantités commandées ou sur quantités livrées). Si elle est basée sur les quantités livrées, la validation du reçu de dropship devrait débloquer la création de la facture sur la commande client.
- Piste à tester : Pour la facturation fournisseur, une fois le reçu de dropship validé, utiliser le bouton standard de création de facture fournisseur (Create Bill) directement depuis la commande d'achat (Purchase Order) confirmée.

_Non couvert_
- La procédure détaillée de création et de validation de la facture client (Customer Invoice) à l'issue d'une livraison en dropshipping n'est pas couverte par les passages fournis.
- La procédure de création et de contrôle de la facture fournisseur (Vendor Bill) sur la commande d'achat liée au dropshipping n'est pas documentée dans les passages fournis.

_Sources :_ [1] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/dropshipping.html#configure-products-to-be-dropshipped · [2] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/dropshipping.html#fulfill-orders-using-dropshipping · [3] applications/inventory_and_mrp/manufacturing/subcontracting/subcontracting_dropship.html#configuration · [7] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/dropshipping.html · [8] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/use_routes.html#additional-routes · [9] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/use_routes.html#on-products · [10] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_one_step.html#create-sales-order

**Note B : ___**

---

## Q7 — 19.0 — Cross-docking (doc absente en 19)

> Comment mettre en place le cross-docking dans un entrepôt en Odoo 19 ?

**Indispensable** : Dire qu'aucune page 19.0 ne décrit le cross-docking. Si la page 18 est utilisée : la marquer « Odoo 18 » et avertir qu'elle n'est pas confirmée pour 19. Éléments génériques 19 (Multi-Step Routes, routes) sourcés en 19. Conseiller une vérification sur une base 19.

**Erreurs à éviter** : Présenter la procédure 18 (route Cross-Dock, réception et livraison en 2 étapes) comme valable en 19 sans avertissement ; inventer des menus.

**Complète** : Lacune explicite + éléments 19 sourcés + page 18 marquée. · **Partielle** : Lacune signalée, mais rien d'utilisable, ou page 18 utilisée avec un avertissement trop discret. · **Incorrecte** : Procédure 18 sans avertissement, ou procédure inventée.

### Réponse A

**Statut : Non couvert** · couverture insufficient

⚠️ Les passages fournis ne documentent pas le cross-docking (route dédiée, règles ni procédure) : ils ne permettent pas de répondre directement. Ils décrivent seulement les briques de base (Multi-Step Routes, réceptions/livraisons en 2 étapes, MTO, routes et règles push/pull). De plus, ils décrivent Odoo 20.0, alors que la question vise Odoo 19.

_Étapes_
1. ⚠️ **Activer Multi-Step Routes** — Aller dans **Inventory app ‣ Configuration ‣ Settings**, section **Warehouse**, cocher **Multi-Step Routes**, puis cliquer sur **Save**. Cela active aussi **Storage Locations**. Ce n'est pas une procédure de cross-docking en soi, mais une brique de base des flux multi-étapes.
2. ⚠️ **Configurer les flux du entrepôt** — Aller dans **Inventory app ‣ Configuration ‣ Warehouses**, ouvrir l'entrepôt, onglet **Warehouse Configuration**, puis choisir les valeurs de **Incoming Shipments** (par ex. **Receive goods in input and then stock (2 steps)**) et de **Outgoing Shipments** (par ex. **Send goods in output and then deliver (2 steps)**). Les emplacements `WH/Input` et `WH/Output` sont créés automatiquement.

_Attention_
- ⚠️ La question vise Odoo 19 : les passages décrivent Odoo 20.0 et la procédure peut différer dans cette version.
- ⚠️ Pour les flux 1, 2 ou 3 étapes, seuls les champs **Incoming Shipments** et **Outgoing Shipments** doivent être réglés ; il ne faut pas créer ni modifier de règles pour ces flux.

_Pistes à tester_
- Piste à tester : combiner la réception en 2 étapes (**Receive goods in input and then stock (2 steps)**) et la livraison en 2 étapes, puis vérifier si le transfert interne WH/Input vers WH/Output peut être déclenché directement par une commande client, sans passage en stock.
- Piste à tester : utiliser la route **Replenish on Order (MTO)** (à activer dans **Inventory app ‣ Configuration ‣ Settings**, section **Logistics**) sur les produits concernés, pour lier le besoin de livraison à un approvisionnement à la commande, puis tester le flux obtenu.
- Piste à tester : créer une route personnalisée avec des règles push/pull (**Routes**) entre l'emplacement d'entrée et l'emplacement de sortie, après avoir activé **Multi-Step Routes** et **Storage Locations**, et la valider en base de test.

_Non couvert_
- Aucun passage ne définit ni ne décrit le cross-docking ni sa configuration native.
- Aucune information sur les règles push/pull précises à créer pour un cross-docking, ni sur la configuration de la route sur le produit.
- Les différences éventuelles entre Odoo 19 et Odoo 20 pour ce sujet ne sont pas couvertes.

_Sources :_ [2] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_two_steps.html#configuration · [8] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/use_routes.html#configuration

**Note A : ___**

### Réponse B

**Statut : Non couvert** · couverture insufficient

⚠️ Les passages documentaires fournis ne couvrent pas spécifiquement la mise en place de la route ou du flux de cross-docking dans Odoo. Toutefois, ils décrivent les prérequis et configurations de base d'un entrepôt qui permettent de gérer les emplacements d'entrée (**WH/Input**) et de sortie (**WH/Output**) via les réceptions et livraisons en deux étapes (**Multi-Step Routes**), ainsi que l'activation du réapprovisionnement à la commande (**Replenish on Order (MTO)**).

_Prérequis_
- ⚠️ Activer la fonctionnalité **Multi-Step Routes** (qui active également **Storage Locations**) pour pouvoir configurer des étapes multiples sur l'entrepôt.

_Étapes_
1. ⚠️ **Activer les routes en plusieurs étapes (Multi-Step Routes)** — Allez dans **Inventory app ‣ Configuration ‣ Settings**. Sous la section **Warehouse**, cochez la case **Multi-Step Routes**, puis cliquez sur **Save** (cela active automatiquement **Storage Locations**).
2. ⚠️ **Configurer les réceptions et livraisons en deux étapes sur l'entrepôt** — Naviguez vers **Inventory app ‣ Configuration ‣ Warehouses** et sélectionnez l'entrepôt à modifier. Sous l'onglet **Warehouse Configuration**, définissez **Incoming Shipments** sur **Receive goods in input and then stock (2 steps)** et **Outgoing Shipments** sur **Send goods in output and then deliver (2 steps)**. Cela crée automatiquement les emplacements `WH/Input` et `WH/Output`.
3. ⚠️ **Activer la route Replenish on Order (MTO) (si nécessaire pour déclencher le flux à la commande)** — Allez dans **Inventory app ‣ Configuration ‣ Settings**. Dans la section **Logistics** en bas de page, cochez **Replenish on Order (MTO)** et cliquez sur **Save**.

_Attention_
- ⚠️ Votre question porte sur Odoo 19, mais les passages documentaires fournis concernent uniquement Odoo 20.0. La procédure et les libellés peuvent différer entre ces deux versions.
- ⚠️ Les réceptions et les livraisons n'ont pas l'obligation d'être configurées avec le même nombre d'étapes (par exemple, il est possible de recevoir en 2 étapes et de livrer en 3 étapes).

_Pistes à tester_
- Piste à tester : Vérifier dans **Inventory app ‣ Configuration ‣ Routes** si une route de Cross-Dock (générée automatiquement lors de la configuration de l'entrepôt en 2 ou 3 étapes) existe ou si elle est archivée par défaut.
- Piste à tester : Une fois l'entrepôt configuré avec `WH/Input` et `WH/Output`, vérifier sur la fiche produit (sous l'onglet **Inventory**, section **Routes**) s'il est possible de cocher une route Cross-Dock en combinaison avec la route d'achat et/ou **Replenish on Order (MTO)** pour transférer directement les produits de `WH/Input` vers `WH/Output` sans passer par `WH/Stock`.

_Non couvert_
- L'existence, le nom exact et l'activation de la route spécifique au cross-docking dans Odoo.
- La configuration exacte des règles au sein de la route de cross-docking (mouvement direct de `WH/Input` vers `WH/Output`).
- L'application de la route de cross-docking sur une fiche produit, une catégorie de produit ou une ligne de commande client.

_Sources :_ [2] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_one_step.html#configuration · [3] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_two_steps.html#configuration · [5] applications/inventory_and_mrp/inventory/warehouses_storage/replenishment/mto.html#enable-the-mto-route · [9] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_two_steps.html

**Note B : ___**

---

## Q8 — 20.0 — Sous-traitance avec fourniture des composants

> En Odoo 20, comment gérer un produit fabriqué par un sous-traitant à qui j'envoie les composants : configuration, bon de commande, envoi des composants et réception du produit fini ?

**Indispensable** : Fabrication → Configuration → Settings → « Subcontracting » ; sous-traitant en fournisseur sur le produit fini ; nomenclature de type sous-traitance avec ses composants (envoyés par défaut au sous-traitant). Flux : bon de commande au sous-traitant → validation de l'ordre de réapprovisionnement (envoi des composants) → réception du produit fini → suivi dans l'historique des mouvements.

**Erreurs à éviter** : Confondre avec la sous-traitance de base (composants déjà chez le sous-traitant) ou avec la sous-traitance en dropship ; demander de créer un ordre de fabrication à la main.

**Complète** : Réglage, fournisseur, nomenclature et les 3 étapes du flux. · **Partielle** : Flux juste, réglage ou type de nomenclature absent. · **Incorrecte** : Mauvais type de sous-traitance, ou étapes inventées.

### Réponse A

**Statut : À vérifier** · couverture partial

⚠️ Dans Odoo 20, le flux de sous-traitance avec réapprovisionnement (*Resupply subcontracting*) permet à une entreprise de fournir ses composants à un sous-traitant afin qu'il fabrique le produit fini et le livre à l'entrepôt de l'entreprise. Les passages fournis documentent l'activation de la sous-traitance, la configuration de la nomenclature (BoM) et des routes sur les composants, ainsi que la création et la confirmation du bon de commande fournisseur (PO) qui génère automatiquement la réception (**Receipt**) et l'ordre de réapprovisionnement (**Resupply**). En revanche, les étapes de traitement de l'envoi des composants et de la réception du produit fini dans ce flux spécifique ne figurent pas dans les extraits fournis.

_Prérequis_
- ⚠️ Le sous-traitant doit être préalablement renseigné comme fournisseur (*vendor*) sur la fiche du produit sous-traité.

_Étapes_
1. ✅ **Activer la fonctionnalité de sous-traitance** — Allez dans **Manufacturing app ‣ Configuration ‣ Settings**, cochez la case **Subcontracting** sous la section **Operations**, puis cliquez sur **Save**.
2. ✅ **Configurer la nomenclature (BoM) du produit sous-traité** — Depuis la fiche du produit sous-traité, cliquez sur le bouton intelligent **Bill of Materials** (ou allez dans **Manufacturing app ‣ Products ‣ Bills of Materials**) et sélectionnez ou créez une nomenclature. Dans le champ **BoM Type**, sélectionnez l'option **Subcontracting**, puis ajoutez un ou plusieurs sous-traitants dans le champ **Subcontractors**. Enfin, dans l'onglet *Components*, cliquez sur **Add a line**, sélectionnez chaque composant dans le menu déroulant **Component** et indiquez la quantité requise dans le champ **Quantity**.
3. ⚠️ **Affecter la route de réapprovisionnement aux composants** — L'activation de la sous-traitance rend disponible la route *Resupply Subcontractor on Order* dans l'application *Inventory*, qui peut être assignée aux produits concernés dans l'onglet *Inventory* de leur fiche produit.
4. ✅ **Créer et confirmer le bon de commande fournisseur (PO)** — Allez dans **Purchase app ‣ Orders ‣ Purchase Orders** et cliquez sur **New**. Sélectionnez le sous-traitant dans le menu déroulant **Vendor**. Dans l'onglet *Products*, cliquez sur **Add a product**, sélectionnez le produit sous-traité et saisissez la quantité dans le champ **Quantity** (le champ **Expected Arrival** se met à jour selon le *Lead Time* du fournisseur). Cliquez sur **Confirm Order** : une réception et un ordre de réapprovisionnement sont automatiquement créés et accessibles via les boutons intelligents **Receipt** et **Resupply** en haut du formulaire.

_Attention_
- ✅ Les composants envoyés chez un sous-traitant restent la propriété de l'entreprise : l'emplacement de sous-traitance étant un emplacement interne, l'expédition des composants vers cet emplacement ne modifie pas la valeur de l'inventaire. Le changement de valeur intervient lors de la réception du produit fini, dont la valeur combine les composants consommés par le sous-traitant et le prix du service de sous-traitance figurant sur le bon de commande.

_Pistes à tester_
- Piste à tester : Pour l'envoi des composants au sous-traitant, cliquer sur le bouton intelligent **Resupply** généré en haut du bon de commande fournisseur (PO) après sa confirmation, puis valider le transfert d'expédition des composants.
- Piste à tester : Pour la réception du produit fini, à l'image du flux de sous-traitance basique, cliquer sur le bouton **Receive** du PO ou sur le bouton intelligent **Receipt** en haut du PO, puis cliquer sur **Validate** (en tenant compte d'éventuels besoins de traçabilité des composants si des numéros de lot/série sont utilisés).

_Non couvert_
- Le détail de la configuration du fournisseur et du délai (*Lead Time*) sur la fiche du produit sous-traité.
- La procédure exacte de traitement et de validation de l'ordre d'envoi des composants (**Resupply**).
- La procédure exacte de réception du produit fini (**Receipt**) spécifique au flux *Resupply subcontracting* (notamment si un enregistrement des composants consommés est requis).

_Sources :_ [2] applications/inventory_and_mrp/manufacturing/subcontracting.html#configuration · [6] applications/inventory_and_mrp/manufacturing/subcontracting/subcontracting_resupply.html · [7] applications/inventory_and_mrp/manufacturing/subcontracting/subcontracting_resupply.html#configure-bom · [9] applications/inventory_and_mrp/manufacturing/subcontracting/subcontracting_resupply.html#create-and-confirm-subcontractor-po · [11] applications/inventory_and_mrp/inventory/inventory_valuation/operations_valuation.html#component-consumption

**Note A : ___**

### Réponse B

**Statut : À vérifier** · couverture partial

⚠️ Pour la sous-traitance avec réapprovisionnement (resupply), on active la sous-traitance, on configure une nomenclature de type Subcontracting avec sous-traitants et composants, puis on crée et confirme un bon de commande, ce qui génère automatiquement une réception et un ordre de réapprovisionnement. Les passages ne détaillent pas la validation de l'envoi des composants (Resupply) ; la réception du produit fini est documentée dans le flux de base.

_Prérequis_
- ✅ Activer le paramètre **Subcontracting** dans **Manufacturing app ‣ Configuration ‣ Settings**, sous **Operations**, puis cliquer sur **Save**.
- ⚠️ Pour que le produit soit sous-traité en resupply, la route *Resupply Subcontractor on Order* est disponible dans l'app Inventory et peut être assignée sur l'onglet **Inventory** de la fiche produit après activation de la sous-traitance.
- ⚠️ Le sous-traitant doit être spécifié comme vendor sur le produit (avec son *Lead Time*, qui alimente l'**Expected Arrival**).

_Étapes_
1. ✅ **Activer la sous-traitance** — Aller dans **Manufacturing app ‣ Configuration ‣ Settings**, cocher **Subcontracting** sous **Operations**, puis **Save**.
2. ✅ **Ouvrir la nomenclature du produit** — Cliquer sur le smart button **Bill of Materials** de la fiche produit, puis sélectionner une nomenclature ou en créer une. Alternative : **Manufacturing app ‣ Products ‣ Bills of Materials**.
3. ✅ **Définir le type de nomenclature et les sous-traitants** — Dans **BoM Type**, choisir **Subcontracting**, puis ajouter un ou plusieurs sous-traitants dans le champ **Subcontractors**.
4. ✅ **Ajouter les composants** — Dans l'onglet *Components*, cliquer sur **Add a line**, choisir le **Component** et renseigner la **Quantity**.
5. ✅ **Créer le bon de commande** — Aller dans **Purchase app ‣ Orders ‣ Purchase Orders**, cliquer sur **New**, choisir le sous-traitant dans **Vendor**.
6. ✅ **Ajouter le produit sous-traité** — Dans l'onglet *Products*, cliquer sur **Add a product**, sélectionner le produit sous-traité et saisir la **Quantity**. Le champ **Expected Arrival** se met à jour selon le *Lead Time* du vendor.
7. ✅ **Confirmer la commande** — Cliquer sur **Confirm Order**. Une réception et un ordre de réapprovisionnement sont créés automatiquement, accessibles via les smart buttons **Receipt** et **Resupply** en haut du formulaire.
8. ⚠️ **Recevoir le produit fini** — Une fois le produit fabriqué par le sous-traitant, cliquer sur **Receive** sur le bon de commande ou sur le smart button **Receipt**, puis sur **Validate** pour entrer le produit en stock (documenté pour la sous-traitance de base, flux de réception identique dans son principe).

_Attention_
- ⚠️ Si des flux d'inventaire à plusieurs étapes sont activés, des transferts supplémentaires doivent être validés pour faire entrer le produit en stock.
- ⚠️ Les composants envoyés au sous-traitant restent la propriété de l'entreprise : l'emplacement de sous-traitance est interne, donc l'envoi ne modifie pas la valeur du stock. La valeur du produit fini change à la réception (composants consommés + prix du service sur le PO).

_Pistes à tester_
- Piste à tester : l'envoi des composants se fait via le transfert lié au smart button **Resupply** du bon de commande, à valider dans l'app Inventory ; à vérifier sur la documentation officielle.
- Piste à tester : vérifier dans **Inventory app ‣ Reporting ‣ Moves History** les mouvements générés après validation de la réception.

_Non couvert_
- Les étapes détaillées de validation de l'ordre de réapprovisionnement (envoi des composants) ne figurent pas dans les passages fournis.
- La configuration détaillée du vendor sur la fiche produit (onglet Purchase, prix, Lead Time) et l'assignation de la route *Resupply Subcontractor on Order* ne sont pas détaillées.

_Sources :_ [2] applications/inventory_and_mrp/manufacturing/subcontracting.html#configuration · [4] applications/inventory_and_mrp/manufacturing/subcontracting/subcontracting_resupply.html · [5] applications/inventory_and_mrp/manufacturing/subcontracting/subcontracting_basic.html#process-receipt · [7] applications/inventory_and_mrp/manufacturing/subcontracting/subcontracting_resupply.html#configure-bom · [9] applications/inventory_and_mrp/manufacturing/subcontracting/subcontracting_resupply.html#create-and-confirm-subcontractor-po · [12] applications/inventory_and_mrp/inventory/inventory_valuation/operations_valuation.html#component-consumption

**Note B : ___**

---

## Q9 — 18.0 — Abonnements (Enterprise)

> En Odoo 18, comment mettre en place des abonnements mensuels et annuels avec paiement automatique par carte, renouvellement et résiliation par le client lui-même ?

**Indispensable** : Plans récurrents (Abonnements → Configuration → Recurring Plans), section Self-Service pour la résiliation ; produit configuré avec un prix par plan (onglet Pricing) ; devis d'abonnement ; fournisseur de paiement compatible avec les paiements automatiques ; échec de paiement (« Payment Failure », « Contract in exception ») ; renouvellement (« Renew » → « Renewal Quotation ») ; résiliation (« Close », « Close Reason ») ; actions planifiées de facturation.

**Erreurs à éviter** : Vocabulaire ancien (« modèles d'abonnement » comme objet de configuration) ; affirmer l'édition Enterprise sans source ; promettre que tous les fournisseurs de paiement gèrent les paiements automatiques.

**Complète** : Les 4 volets (plans, paiement auto, renouvellement, résiliation) sourcés 18.0. · **Partielle** : Un volet manquant ou non sourcé sans le signaler. · **Incorrecte** : Terminologie ou menus d'une autre version, échec de paiement inventé.

### Réponse A

**Statut : À vérifier** · couverture partial

⚠️ L'application **Subscriptions** d'Odoo permet de gérer les abonnements mensuels (**Monthly**) et annuels (**Yearly**), avec facturation et renouvellements automatisés, paiements automatiques par carte via un prestataire prenant en charge la tokenisation, ainsi que la résiliation en libre-service par le client depuis son portail. Notez que la procédure décrite ci-dessous s'appuie sur la documentation d'Odoo 20.0 (et non d'Odoo 18). De plus, si le principe des renouvellements automatiques est bien confirmé, le détail du paramétrage exact déclenchant le renouvellement n'est pas précisé dans les extraits fournis.

_Prérequis_
- ⚠️ Disposer de l'application **Subscriptions** (qui s'intègre avec **Invoicing**, **Sales**, **CRM** et **Helpdesk**).
- ✅ Pour les paiements automatiques : choisir et configurer un prestataire de paiement qui prend en charge la tokenisation (Adyen, Authorize.net, Flutterwave, Razorpay, Stripe ou Xendit).
- ✅ Pour les paiements automatiques : avoir mis en place un portail client ou un site **eCommerce** (ce dernier nécessite l'application **Website**).

_Étapes_
1. ✅ **Configurer le prestataire de paiement pour le prélèvement automatique** — Choisissez un prestataire compatible avec la tokenisation (Adyen, Authorize.net, Flutterwave, Razorpay, Stripe, Xendit), créez un compte auprès de lui et configurez ses identifiants API dans Odoo. Activez ensuite le prestataire de paiement, configurez ses méthodes de paiement et activez la tokenisation.
2. ✅ **Vérifier ou créer les plans récurrents (mensuel et annuel) et activer la résiliation client** — Allez dans **Subscriptions app ‣ Configuration ‣ Recurring Plans**. Par défaut, des plans courants comme **Monthly** et **Yearly** sont déjà disponibles. Sélectionnez un plan existant pour le modifier ou cliquez sur **New** pour en créer un (en renseignant **Name**, **DETAILS**, **SELF-SERVICE** et **Pricing**). Dans la section **Self-Service** du formulaire **Recurring Plans**, activez l'option **Closable** : cela ajoute un menu déroulant permettant de définir si l'abonnement peut être clôturé à la date choisie par l'utilisateur ou à la fin de la période de renouvellement en cours.
3. ✅ **Configurer les motifs de résiliation (optionnel)** — Les clients devant obligatoirement choisir un motif préconfiguré sur le portail lors de la résiliation, vous pouvez créer des motifs personnalisés en allant dans **Subscriptions app ‣ Configuration ‣ Close Reasons**.
4. ✅ **Créer et configurer le produit d'abonnement** — Naviguez vers **Subscriptions app ‣ Products ‣ Products**, puis cliquez sur **New** (ou sélectionnez un produit existant). Assurez-vous que les options **Subscriptions** (activée par défaut) et **Sales** restent cochées. Dans l'onglet **General Information**, configurez : **Product type** (généralement **Service**, ou `Goods` pour un bien physique), **Invoicing policy** (moment où le client est facturé ; obligatoirement **Ordered quantities** pour les biens physiques), **Unit of Measure** (généralement **Units**) et **Sales Price**.
5. ✅ **Définir les tarifs mensuels et annuels sur le produit** — Dans l'onglet **Recurring Prices** de la fiche produit, cliquez sur **Add a price rule** (ou **Add a line** sous l'onglet **Recurring prices**) pour ajouter chaque plan récurrent souhaité (par exemple **Monthly** et **Yearly**) et définir le prix correspondant.
6. ✅ **Publier le produit sur le site eCommerce (si vente en ligne)** — Si l'abonnement est vendu via **eCommerce**, cliquez sur le bouton intelligent **Go To Website** sur la fiche produit, puis dans l'en-tête de la page, basculez le curseur gris de **Unpublished** au statut vert **Published**.
7. ⚠️ **Enregistrement du moyen de paiement par le client** — Lors du passage de commande en ligne (checkout) ou directement en se connectant à son portail client, le client saisit et enregistre ses informations de carte bancaire. Le prestataire crée alors un jeton (token) qui sera utilisé pour les paiements récurrents automatiques.
8. ✅ **Résiliation en libre-service par le client** — Pour résilier, le client se connecte à son portail utilisateur, clique sur le bouton **Subscriptions** sur la page d'accueil, puis clique sur son abonnement. Sur la page de détail, il clique sur **Close Subscription**, sélectionne un motif dans la fenêtre pop-up **Close Subscription**, et clique sur **Submit**. L'abonnement passe au statut **Closed** sur le portail et *Churned* dans la base de données (l'administrateur peut prévisualiser cette interface via le bouton **Preview** en haut de la commande d'abonnement).

_Attention_
- ⚠️ Différence de version : votre question porte sur Odoo 18, mais la présente réponse repose exclusivement sur la documentation officielle d'Odoo 20.0. Certaines interfaces, libellés ou fonctionnalités peuvent différer dans Odoo 18.
- ✅ L'unité de mesure `Days` ne peut pas être utilisée comme **Billing Period** pour les produits d'abonnement (elle est réservée aux locations / rentals afin d'éviter la génération de factures quotidiennes).
- ✅ Pour un abonnement portant sur un bien physique, le champ **Invoicing Policy** doit impérativement être configuré sur **Ordered quantities**, sous peine de générer des erreurs lors de la création des factures.
- ✅ Si le client choisit de ne pas enregistrer ses informations de paiement (lorsque le prestataire laisse le choix au moment du paiement), les paiements automatiques ne pourront pas fonctionner.
- ✅ Depuis le portail utilisateur, le client ne peut pas saisir un motif de résiliation libre (custom reason) : il doit obligatoirement choisir parmi les motifs préconfigurés par l'administrateur.

_Pistes à tester_
- Piste à tester : Vérifier dans les champs dessections **DETAILS** et **SELF-SERVICE** du formulaire **Subscriptions app ‣ Configuration ‣ Recurring Plans** quels paramètres permettent de piloter le comportement exact du renouvellement automatique et de la facturation récurrente.
- Piste à tester : Vérifier le chemin exact dans l'application **Invoicing** ou **Website** pour activer le prestataire de paiement et cocher l'option de tokenisation.

_Non couvert_
- Le détail des champs situés dans la section **DETAILS** du formulaire **Recurring Plans** (notamment le paramétrage précis de la durée, de l'échéance de facturation et du déclenchement du renouvellement automatique).
- Le chemin de menu exact dans Odoo pour accéder à la configuration des prestataires de paiement (**Payment Providers**) et y activer la tokenisation.

_Sources :_ [1] applications/sales/subscriptions.html · [2] applications/sales/subscriptions.html#set-up-recurring-plans · [3] applications/sales/subscriptions/automatic_payments.html#setting-up-a-payment-processor-that-supports-automatic-payments · [4] applications/sales/subscriptions.html#product-form-configuration · [5] applications/sales/subscriptions/closing.html#configuration · [7] applications/sales/subscriptions/automatic_payments.html · [8] applications/sales/subscriptions/subscriptions_deliveries.html#creating-a-subscription-delivery-product · [9] applications/sales/subscriptions/automatic_payments.html#how-customers-can-set-up-automatic-payments · [10] applications/sales/subscriptions/renewals.html · [11] applications/sales/subscriptions/closing.html#customer-view

**Note A : ___**

### Réponse B

**Statut : À vérifier** · couverture partial

⚠️ Les passages décrivent Odoo 20 (la question vise Odoo 18, la procédure peut différer). Ils couvrent : les plans récurrents Monthly/Yearly, la fiche produit d'abonnement, le paiement automatique par fournisseur supportant la tokenisation, la résiliation par le client via le portail et la vente en eCommerce. Le renouvellement n'est décrit que de façon générale, sans procédure détaillée.

_Prérequis_
- ⚠️ Configurer d'abord les plans récurrents (anciennement « recurrence periods ») ; l'app Subscriptions inclut par défaut des plans courants comme Monthly et Yearly.
- ⚠️ Utiliser un fournisseur de paiement qui supporte la tokenisation (Adyen, Authorize.net, Flutterwave, Razorpay, Stripe, Xendit).
- ⚠️ Le paiement automatique nécessite en plus un portail client ou un site eCommerce.

_Étapes_
1. ⚠️ **Vérifier ou créer les plans récurrents** — Aller dans **Subscriptions app ‣ Configuration ‣ Recurring Plans**. Les plans **Monthly** et **Yearly** existent par défaut ; pour en créer un, cliquer sur **New** et renseigner **Name**, **DETAILS**, **SELF-SERVICE** et **Pricing**. L'unité **Days** ne peut pas servir de **Billing Period**.
2. ⚠️ **Créer le produit d'abonnement** — Aller dans **Subscriptions app ‣ Products ‣ Products**, ouvrir un produit existant ou cliquer sur **New**. Laisser activées les options **Subscriptions** et **Sales**. Dans l'onglet **General Information**, configurer **Product type** (typiquement **Service**), l'invoicing policy, **Unit of Measure** et **Sales Price**.
3. ⚠️ **Définir les prix récurrents mensuel et annuel** — Dans l'onglet **Recurring Prices**, cliquer sur **Add a price rule** pour chaque option (une ligne pour le plan mensuel, une pour l'annuel).
4. ⚠️ **Configurer le fournisseur de paiement** — Choisir un fournisseur supportant la tokenisation, suivre son guide de configuration pour créer le compte et saisir les identifiants API dans Odoo, puis activer le fournisseur, configurer ses méthodes de paiement et sa tokenisation.
5. ⚠️ **Autoriser l'enregistrement des moyens de paiement** — Dans l'onglet **Configuration** du fournisseur de paiement, activer **Allow Saving Payment Methods** : un token de paiement est créé et réutilisé pour les paiements suivants sans ressaisie des données.
6. ⚠️ **Publier le produit sur l'eCommerce (si vente en ligne)** — Sur la fiche produit, cliquer sur le smart button **Go To Website**, puis faire passer le curseur de **Unpublished** à **Published**. Les périodes récurrentes configurées sont alors proposées à l'achat.
7. ⚠️ **Autoriser la résiliation par le client** — Aller dans **Subscriptions app ‣ Configuration ‣ Recurring Plans**, ouvrir ou créer un plan, puis activer **Closable** dans la section **Self-Service**. Un menu déroulant permet de clore à la date choisie par l'utilisateur ou à la fin de la période de renouvellement en cours.
8. ⚠️ **Résiliation côté client dans le portail** — Le client clique sur **Subscriptions** dans le portail, ouvre son abonnement, clique sur **Close Subscription**, choisit un motif préconfiguré dans le pop-up puis clique sur **Submit**. L'abonnement est alors **Closed** dans le portail et marqué *Churned* dans la base. Les motifs se créent dans **Subscriptions app ‣ Configuration ‣ Close Reasons**.

_Attention_
- ✅ La question vise Odoo 18 : les passages décrivent Odoo 20 et la procédure peut différer dans cette version (par ex. le terme « Recurring Plans », anciennement « recurrence periods »).
- ⚠️ Le client ne peut pas saisir de motif libre lors de la résiliation depuis le portail : il doit choisir un motif préconfiguré.
- ⚠️ Pour un produit physique, une mauvaise **Invoicing Policy** provoque des erreurs de facturation : elle doit être **Ordered quantities**.
- ⚠️ Par défaut, l'app génère automatiquement devis et factures ; le paiement automatique demande une configuration supplémentaire.

_Non couvert_
- Procédure détaillée du renouvellement (automatique ou manuel) : les passages n'en donnent qu'une description générale, sans menus ni réglages.
- Réglage précis pour déclencher le prélèvement automatique par carte à chaque échéance au-delà de la tokenisation.
- Différences exactes de la procédure dans Odoo 18.

_Sources :_ [2] applications/sales/subscriptions.html#set-up-recurring-plans · [3] applications/sales/subscriptions/automatic_payments.html#setting-up-a-payment-processor-that-supports-automatic-payments · [4] applications/sales/subscriptions.html#product-form-configuration · [5] applications/sales/subscriptions/closing.html#configuration · [6] applications/sales/subscriptions/renewals.html · [7] applications/sales/subscriptions/automatic_payments.html · [9] applications/finance/payment_providers.html#tokenization · [10] applications/sales/subscriptions/ecommerce.html · [11] applications/sales/subscriptions/closing.html#customer-view

**Note B : ___**

---

## Q10 — 20.0 — Transactions inter-sociétés

> Deux sociétés du même groupe sur une même base Odoo 20 : comment faire pour qu'une commande de vente de la société A crée automatiquement l'achat correspondant dans la société B, avec les mouvements de stock et les factures ?

**Indispensable** : Accès des utilisateurs aux deux sociétés ; « Inter-Company Transactions » activé dans les paramètres (section Companies) ; options « Create Sales Orders », « Create Purchase Orders » (avec « Use Warehouse »), « Create Vendor Bills », « Synchronize Stock Moves », option de validation automatique ; entrepôts à créer à la main pour les sociétés ajoutées après la mise en place ; accès aussi par la fiche société (onglet visible en mode développeur) ; compensation via le module `account_payment_interco`, activé dans chaque société.

**Erreurs à éviter** : Inverser le sens (régler l'option dans A) ; affirmer que les entrepôts sont créés automatiquement ; affirmer l'édition sans source. La page elle-même mélange deux libellés (« Create Vendor Bills » / « Create Bills and Refunds », « Validated » / « Create and validate ») : les deux sont acceptés.

**Complète** : Réglage dans la bonne société, options associées au bon sens, note sur les entrepôts, factures et compensation. · **Partielle** : Réglage juste, mais stock ou factures non traités. · **Incorrecte** : Sens inversé, options inventées.

### Réponse A

**Statut : À vérifier** · couverture complete

⚠️ Dans Odoo 20.0, la fonctionnalité **Inter-Company Transactions** permet à deux sociétés d'une même base de données de se vendre et de s'acheter des biens ou des services en générant et synchronisant automatiquement les documents de contrepartie (commandes d'achat à partir des commandes de vente, factures fournisseurs à partir des factures clients, et mouvements de stock).

_Prérequis_
- ⚠️ Les enregistrements de produits doivent être partagés entre les sociétés impliquées.
- ✅ Les configurations générales et spécifiques, notamment les positions fiscales et les localisations, doivent être correctement paramétrées.
- ⚠️ Chaque société doit disposer de son propre entrepôt : Odoo ne crée pas automatiquement d'entrepôt pour les sociétés ajoutées après l'initialisation de la base, ils doivent donc être créés manuellement.

_Étapes_
1. ✅ **Sélectionner la société et activer les transactions inter-sociétés** — Sélectionnez la société concernée dans le sélecteur de société, ouvrez l'application **Settings**, naviguez jusqu'à la section **Companies**, activez **Inter-Company Transactions**, puis cliquez sur **Save**.
2. ⚠️ **Activer la création automatique des commandes d'achat** — Cochez l'option **Create Purchase Orders** pour créer automatiquement une demande de prix (commande d'achat en brouillon) lorsqu'une commande de vente est confirmée pour la société sélectionnée, et renseignez l'entrepôt de la société dans le champ **Use Warehouse** qui apparaît.
3. ⚠️ **Activer la synchronisation des mouvements de stock** — Cochez l'option **Synchronize Stock Moves** pour synchroniser automatiquement les mouvements de stock entre les sociétés lors du traitement des livraisons ou des réceptions pour la société sélectionnée.
4. ✅ **Activer la création automatique des factures fournisseurs** — Cochez l'option **Create Vendor Bills** pour créer automatiquement une facture fournisseur ou un avoir fournisseur lorsqu'une société confirme une facture client ou un avoir pour la société sélectionnée.
5. ✅ **Définir la validation automatique et enregistrer** — Si vous souhaitez que les enregistrements générés soient automatiquement validés, sélectionnez **Validated** (ce paramètre s'applique à toutes les options de transactions inter-sociétés), puis cliquez sur **Save**. Notez que ces paramètres sont aussi accessibles via **Settings ‣ Users & Companies ‣ Companies** dans l'onglet **Inter-Company Transactions** après avoir activé le mode développeur.

_Attention_
- ✅ Le choix de l'option **Validated** pour valider automatiquement les enregistrements générés s'applique globalement à toutes les options de transactions inter-sociétés sélectionnées.
- ⚠️ Le champ **Use Warehouse** apparaît lorsqu'on sélectionne **Create Sales Orders** ou **Create Purchase Orders**, mais les entrepôts des sociétés supplémentaires créées après la configuration initiale de la base ne sont pas créés automatiquement par Odoo et doivent être créés manuellement.

_Sources :_ [1] applications/general/companies/multi_company.html#inter-company-transactions

**Note A : ___**

### Réponse B

**Statut : À vérifier** · couverture partial

✅ Dans Odoo 20, on active **Inter-Company Transactions** dans **Settings** pour la société concernée, puis on coche les options de contrepartie : **Create Purchase Orders** (commande de vente confirmée → demande de prix/achat), **Synchronize Stock Moves** (mouvements de stock) et **Create Vendor Bills** (factures). L'option **Validated** permet la validation automatique. Les passages ne précisent pas dans le détail quelle société doit porter quelle option ; le sens de la contrepartie est illustré par l'exemple documenté.

_Prérequis_
- ✅ Les deux sociétés doivent exister dans la même base (création/édition via **Settings app ‣ Users & Companies ‣ Companies**, bouton **New**).
- ⚠️ Un entrepôt doit exister pour chaque société : Odoo ne crée pas automatiquement d'entrepôt pour les sociétés ajoutées après la configuration initiale de la base ; il faut les créer manuellement (le champ **Use Warehouse** apparaît avec **Create Sales Orders** ou **Create Purchase Orders**).
- ✅ Les configurations générales et spécifiques (positions fiscales, localisations) doivent être correctement paramétrées pour que les transactions inter-sociétés fonctionnent.
- ✅ Les fiches produits sont partagées entre les sociétés impliquées dans les transactions inter-sociétés.

_Étapes_
1. ✅ **Sélectionner la société** — Dans le sélecteur de sociétés, sélectionner la société concernée (celle pour laquelle on active la fonction).
2. ✅ **Activer la fonction** — Ouvrir l'app **Settings**, aller à la section **Companies**, activer **Inter-Company Transactions** puis cliquer sur **Save**.
3. ⚠️ **Créer l'achat à partir de la vente** — Cocher **Create Purchase Orders** : une demande de prix (achat en brouillon) est créée automatiquement quand une commande de vente est confirmée pour la société sélectionnée, en utilisant l'entrepôt choisi dans **Use Warehouse**.
4. ⚠️ **Synchroniser les mouvements de stock** — Cocher **Synchronize Stock Moves** pour synchroniser automatiquement les mouvements de stock entre sociétés lors des livraisons/réceptions.
5. ✅ **Générer les factures de contrepartie** — Cocher **Create Vendor Bills** : une facture/avoir fournisseur est créé automatiquement quand une société confirme une facture/avoir client pour la société sélectionnée.
6. ⚠️ **Choisir la validation automatique (optionnel)** — Sélectionner **Validated** pour valider automatiquement les documents créés ; ce réglage s'applique à toutes les options inter-sociétés.
7. ⚠️ **Vérifier via la fiche société (alternative)** — Les réglages sont aussi accessibles via **Settings ‣ Users & Companies ‣ Companies** en sélectionnant la société ; en mode développeur, l'onglet **Inter-Company Transactions** apparaît.

_Attention_
- ✅ Une configuration incorrecte (positions fiscales, localisations) peut empêcher le bon traitement des transactions inter-sociétés.
- ✅ Odoo ne crée pas automatiquement les entrepôts des sociétés ajoutées après l'installation initiale : à créer manuellement.
- ✅ Le réglage **Validated** s'applique à toutes les options inter-sociétés, pas à une seule.

_Pistes à tester_
- Piste à tester : réaliser le paramétrage pour chaque société impliquée (A et B) via le sélecteur de sociétés, puis tester un cycle complet vente → achat → livraison/réception → facture pour vérifier le sens des contreparties.
- Piste à tester : si le règlement inter-sociétés est nécessaire, vérifier le module **Intercompany Payment - Account** (`account_payment_interco`) et ses comptes de compensation (**Accounting ‣ Configuration ‣ Settings**, section **Default Accounts**, **Intercompany Clearing**).

_Non couvert_
- Le détail du comportement des mouvements de stock synchronisés (étapes, routes, lots) n'est pas documenté dans les passages.
- Les réglages précis de positions fiscales, de devises et de tarifs pour les transactions inter-sociétés ne sont pas détaillés.

_Sources :_ [1] applications/general/companies/multi_company.html#inter-company-transactions · [3] applications/general/companies/multi_company.html#create-or-edit-a-company

**Note B : ___**

---

## Q11 — 19.0 — Location avec caution (Enterprise)

> En Odoo 19, comment louer du matériel avec une caution encaissée à la réservation et remboursée au retour, y compris le suivi de l'enlèvement et du retour ?

**Indispensable** : Produit de caution créé dans Location → Products, ajouté en produit optionnel du produit loué ; commande de location avec période ; enlèvement et retour ; remboursement par **avoir** depuis la facture, et quantité livrée remise à 0 sur la commande.

**Erreurs à éviter** : Citer la page 18 (`rental/manage_deposits`, autre chemin) pour une question 19 ; inventer une case « caution » sur le produit loué ; rembourser sans avoir.

**Complète** : Configuration de la caution, flux de location et remboursement par avoir + quantité livrée à 0. · **Partielle** : Remboursement mentionné sans la mécanique avoir + quantité livrée. · **Incorrecte** : Mécanique inventée, ou page 18 non signalée.

### Réponse A

**Statut : À vérifier** · couverture complete

⚠️ Pour gérer la location de matériel avec une caution (dépôt de garantie), il est nécessaire de créer un produit de type service distinct dédié à la caution, facturé sur les quantités livrées manuelles. Une fois la commande de location confirmée, la caution est facturée et encaissée en passant sa quantité livrée à 1. Le suivi du matériel s'effectue via les boutons d'enlèvement (**Pickup**) et de retour (**Return**) sur la commande. Au retour du matériel, le remboursement de la caution est traité en émettant un avoir sur la facture de caution, en remettant la quantité livrée de la caution à 0 sur la commande, puis en imputant l'avoir sur la facture finale.

_Prérequis_
- ⚠️ L'application **Rental** doit être utilisée pour gérer les commandes, les enlèvements et les retours.
- ✅ L'application **Accounting** doit être installée pour pouvoir traiter le remboursement de la caution au retour.
- ✅ Pour chaque produit de location nécessitant une caution, un second produit dédié spécifiquement à la caution doit obligatoirement être configuré.
- ✅ Si le produit physique loué est suivi par numéro de série, la fonctionnalité *Lots & Serial Numbers* doit être activée dans l'application **Inventory** et le champ *Tracking* doit être défini sur *By Unique Serial Number* sur la fiche du produit.

_Étapes_
1. ✅ **Configurer le produit de caution** — Allez dans **Rental ‣ Products ‣ Products**, cliquez sur **New** et nommez clairement le produit comme une caution. Définissez le champ **Product Type** sur **Service**, le champ **Invoicing Policy** sur **Based on Delivered Quantity (Manual)**, le champ **Sales Price** sur le montant souhaité de la caution et l'unité de mesure sur **Units**. Choisissez d'inclure ou non les taxes de vente, puis cliquez sur **(save)**.
2. ✅ **Facturer et encaisser la caution à la confirmation** — Une fois la commande de location confirmée (avant ou au moment de l'enlèvement), modifiez la colonne **Delivered** du produit de service de caution à `1` (le texte passe du noir au bleu). Cliquez sur **Create Invoice**, sélectionnez **Regular invoice** dans la fenêtre *Create invoice(s)*, puis cliquez sur **Create Draft**. Après vérification, cliquez sur **Confirm**, puis sur **Send** (ou pour une transaction en personne, cliquez sur **Pay**, vérifiez la fenêtre *Pay*, cliquez sur **Create Payment** puis sur **Send**).
3. ✅ **Enregistrer l'enlèvement du matériel (Pickup)** — Allez dans **Rental app ‣ Orders ‣ Orders** et sélectionnez la commande de location. Cliquez sur **Pickup** pour ouvrir la fenêtre *Validate a pickup*. Si le produit physique a le suivi activé, cliquez dans la colonne **Serial Numbers** et sélectionnez le numéro de série dans la liste déroulante. Cliquez sur **Validate** : cela applique le badge **Picked-up** à la commande et met à jour la colonne **Delivered**.
4. ✅ **Enregistrer le retour du matériel (Return)** — Lorsque le client rapporte le matériel, allez dans **Rental app ‣ Orders ‣ Orders**, sélectionnez la commande et cliquez sur **Return**. Dans la fenêtre *Validate a return*, vérifiez les quantités dans les colonnes **Product**, **Picked-up** et **Returned**, puis cliquez sur **Validate** pour appliquer le badge **Returned** et mettre à jour la colonne **Returned**.
5. ✅ **Émettre un avoir sur la facture de caution** — Depuis la commande dans **Rental app ‣ Orders ‣ Orders**, cliquez sur le bouton intelligent **Invoices**, trouvez la facture correspondant à la caution et émettez un avoir (credit note). Par exemple, renseignez le motif dans le champ **Reason displayed on Credit Note** de la fenêtre *Credit Note*.
6. ✅ **Mettre à jour la ligne de caution et créer la facture finale** — Revenez à la commande de location via le bouton intelligent **Sales Orders**. Sur la ligne de commande de la caution, passez la quantité **Delivered** de `1` à `0` pour marquer la caution comme retournée. Vérifiez les éventuels remboursements de location dus, puis cliquez sur **Create Invoice** pour facturer les frais restants.
7. ✅ **Imputer l'avoir sur la facture finale** — Dans le brouillon de la facture finale (où la ligne de caution apparaît avec un montant négatif), consultez la section **Outstanding Credits** en bas de page pour retrouver l'avoir créé pour la caution, puis cliquez sur **Add** pour appliquer ce crédit à la facture et finaliser le processus de remboursement.

_Attention_
- ⚠️ Votre question porte sur Odoo 19.0, mais les passages fournis décrivent exclusivement la documentation officielle d'Odoo 20.0. La procédure et certains libellés peuvent différer en version 19.0.
- ✅ Si un produit de location physique est loué conjointement avec un produit de location de type service, les deux doivent obligatoirement être retournés sur la commande de location.

_Sources :_ [1] applications/sales/rental/rental_orders/manage_deposits.html#refund-deposits-upon-return · [3] applications/sales/rental/rental_orders/manage_deposits.html#configuration · [4] applications/sales/rental/rental_orders/manage_deposits.html#process-a-deposit-on-a-rental-order · [5] applications/sales/rental/rental_orders/pickup_return.html#pick-up-a-rental-product · [6] applications/sales/rental/rental_orders/pickup_return.html#return-a-rental-product · [7] applications/sales/rental.html · [11] applications/sales/rental/rental_orders/pickup_return.html#pick-up-a-physical-rental-product-with-tracking-enabled

**Note A : ___**

### Réponse B

**Statut : À vérifier** · couverture partial

✅ Les passages (Odoo 20) décrivent le flux complet : produit de caution distinct, facturation de la caution à l'enlèvement ou avant, enlèvement (Pickup), retour (Return), puis remboursement via une note de crédit. La caution est facturée « avant ou au moment de l'enlèvement », pas explicitement à la réservation. La question vise Odoo 19 : la procédure peut différer.

_Prérequis_
- ✅ L'application Accounting doit être installée pour traiter le remboursement de la caution.
- ⚠️ Pour configurer les paramètres de devis, l'application Sales doit être installée.
- ✅ Pour chaque produit de location nécessitant une caution, un second produit de service dédié à la caution doit être configuré.
- ✅ Pour un produit suivi par numéro de série : la fonction Lots & Serial Numbers de l'application Inventory doit être activée et le champ Tracking réglé sur By Unique Serial Number sur la fiche produit.

_Étapes_
1. ✅ **Créer le produit de caution** — Aller dans **Rental ‣ Products ‣ Products**, cliquer sur **New** et nommer clairement le produit de service comme une caution (inclure le nom du produit loué est conseillé).
2. ✅ **Configurer le produit de caution** — Définir **Product Type** sur **Service**, **Invoicing Policy** sur **Based on Delivered Quantity (Manual)**, **Sales Price** au montant de la caution, l'unité de mesure sur **Units**. Choisir d'inclure ou non les taxes de vente, puis enregistrer.
3. ⚠️ **Confirmer l'ordre de location** — Un devis confirmé devient un ordre de location (rental order) ; les produits ne peuvent être enlevés qu'après cette confirmation. Ajouter la ligne de caution à l'ordre.
4. ✅ **Facturer la caution** — Avant ou au moment de l'enlèvement, passer la colonne **Delivered** de la ligne de caution à `1`, cliquer sur **Create Invoice**, choisir **Regular invoice**, puis **Create Draft**. Après vérification, cliquer sur **Confirm**, puis **Send**.
5. ✅ **Encaisser la caution** — Si le client est présent, cliquer sur **Pay**, vérifier la fenêtre *Pay*, cliquer sur **Create Payment**, puis **Send** pour envoyer le reçu. Sélectionner un **Journal** dans la fenêtre **Pay**. Cliquer ensuite sur le smart button **Payments** de l'ordre et sur **Validate** sur la page du paiement.
6. ✅ **Enregistrer l'enlèvement** — Aller dans **Rental app ‣ Orders ‣ Orders**, ouvrir l'ordre, cliquer sur **Pickup**, vérifier la fenêtre *Validate a pickup* puis cliquer sur **Validate**. L'ordre reçoit le badge **Picked-up** et la colonne **Delivered** est mise à jour. Avec suivi par numéro de série, choisir le numéro dans la colonne **Serial Numbers** avant de valider.
7. ✅ **Enregistrer le retour** — Au retour du client, dans **Rental app ‣ Orders ‣ Orders**, ouvrir l'ordre, cliquer sur **Return**, vérifier la fenêtre *Validate a return* puis cliquer sur **Validate**. Le badge **Returned** s'applique. Un service de location associé doit aussi être retourné sur l'ordre.
8. ✅ **Créer la note de crédit de la caution** — Dans l'ordre de location, cliquer sur le smart button **Invoices**, trouver la facture de caution et émettre une note de crédit (ex. `Security Deposit Refund` dans **Reason displayed on Credit Note**).
9. ✅ **Marquer la caution comme retournée** — Revenir à l'ordre via le smart button **Sales Orders** et passer la quantité **Delivered** de la ligne de caution de `1` à `0`.
10. ✅ **Facture finale et application du crédit** — Examiner les remboursements de location dus, cliquer sur **Create Invoice** pour les charges restantes. Dans le brouillon, la ligne de caution apparaît en négatif. Dans **Outstanding Credits**, cliquer sur **Add** pour appliquer la note de crédit : le remboursement est terminé.

_Attention_
- ⚠️ La question vise Odoo 19 alors que les passages décrivent Odoo 20 : la procédure peut différer dans cette version.
- ✅ La caution est facturée avant ou au moment de l'enlèvement, selon la documentation, et non explicitement à la réservation.
- ✅ Le deuxième produit dédié à la caution est obligatoire pour chaque produit de location avec caution.
- ⚠️ Si la fonction Rental Transfers est activée, ne pas modifier l'emplacement Customer/Rental pour ne pas corrompre le suivi de stock.

_Pistes à tester_
- Piste à tester : pour encaisser la caution dès la réservation, facturer et payer la ligne de caution juste après la confirmation de l'ordre, avant l'enlèvement, en suivant la même procédure de facturation.
- Piste à tester : activer **Rental Transfers** dans **Rental app ‣ Configuration ‣ Settings** pour obtenir un suivi de stock à l'enlèvement et au retour.

_Non couvert_
- Procédure spécifique à Odoo 19 non couverte.
- Encaissement automatique de la caution lors de la réservation (ex. boutique en ligne) non documenté dans les passages.

_Sources :_ [1] applications/sales/rental/rental_orders/manage_deposits.html#refund-deposits-upon-return · [2] applications/sales/rental/rental_orders/manage_deposits.html#configuration · [3] applications/sales/rental/rental_orders/manage_deposits.html#process-a-deposit-on-a-rental-order · [4] applications/sales/rental/rental_orders/create_rental_order.html#confirm-and-pay · [5] applications/sales/rental/rental_orders/pickup_return.html#pick-up-a-physical-rental-product-with-tracking-enabled · [6] applications/sales/rental/rental_orders/pickup_return.html#return-a-rental-product · [9] applications/sales/rental/rental_orders/create_rental_order.html · [10] applications/sales/rental/rental_orders/pickup_return.html#pick-up-a-rental-product · [11] applications/sales/rental/configure_products/products.html#rental-transfers-feature

**Note B : ___**

---

## Q12 — 20.0 — Emballages consignés (doc insuffisante)

> En Odoo 20, comment gérer des emballages consignés (palettes, fûts) facturés au client avec la marchandise, remboursés quand il les rapporte, avec un solde de consignes par client ?

**Indispensable** : Dire clairement que la doc officielle ne couvre pas la consigne ni le solde par client. Séparer ce qui est sourcé (retours, avoirs) de ce qui est proposé. Toute piste (produit « consigne », retour, avoir, rapport) marquée « non vérifié ». Recommander un test sur base, voire un développement ou un module tiers, présentés comme options et non comme du standard.

**Erreurs à éviter** : Inventer un réglage ou un module standard « Consignes » ; présenter la caution de la Location comme la solution standard ; confondre « Packaging » (conditionnement) et emballage consigné ; inventer un rapport de solde.

**Complète** : Lacune explicite + pistes étiquetées « non vérifié » + sources connexes justes. · **Partielle** : Lacune signalée, mais des pistes présentées comme sourcées. · **Incorrecte** : Procédure affirmée comme standard sans source.

### Réponse A

**Statut : À vérifier** · couverture partial

✅ La documentation fournie ne décrit pas de flux natif complet de consigne d'emballages (palettes, fûts) facturée avec la marchandise, remboursée au retour, avec solde par client. Elle documente des briques voisines : le réglage Consignment (stock en consignation, un autre sujet), les packagings/packages, le retour avec Reverse Transfer + Credit Note, et le remboursement d'une caution dans Rental. Ces éléments permettent seulement de bâtir une solution à tester.

_Prérequis_
- ⚠️ Pour les retours après facturation : applications Sales, Inventory et Accounting (les Credit Notes nécessitent Accounting ; les Reverse Transfers nécessitent Inventory).
- ⚠️ Pour utiliser des packages : activer la fonction **Packages** sous **Inventory app ‣ Configuration ‣ Settings**, rubrique **Operations**, puis **Save**.

_Étapes_
1. ⚠️ **Activer les packages (optionnel)** — Aller dans **Inventory app ‣ Configuration ‣ Settings**, rubrique **Operations**, activer **Packages**, puis cliquer sur **Save**. Les packages servent à regrouper ou expédier des produits ; ils ne gèrent pas de consigne financière.
2. ✅ **Retour de l'emballage : créer le Reverse Transfer** — Dans l'app **Sales**, ouvrir la commande, cliquer sur le smart button **Delivery**, puis sur **Return** pour ouvrir le pop-up **Reverse Transfer**. Modifier **Product** et/ou **Quantity** si besoin, puis cliquer sur **Return**. L'entrepôt valide ensuite la réception avec **Validate**.
3. ✅ **Rembourser : émettre une Credit Note** — Depuis la commande, ouvrir la facture via le smart button **Invoices**, puis cliquer sur **Credit Note**. Renseigner **Reason displayed on Credit Note**, **Journal** et **Reversal Date**, cliquer sur **Reverse** ou **Reverse and Create Invoice**, puis **Confirm**.
4. ⚠️ **Consulter le solde par client (comptabilité générale)** — Le rapport **Partner Ledger** affiche le solde des clients et fournisseurs : **Accounting ‣ Reporting ‣ Partner Ledger**.

_Attention_
- ✅ Le réglage **Consignment** (Inventory ‣ Configuration ‣ Settings, section **Traceability**) concerne la réception, le stockage et la vente de stock en consignation, pas les emballages consignés facturés au client.
- ✅ Le flux de remboursement de caution (Credit Note sur la facture de caution, **Delivered** passé de 1 à 0) est documenté pour l'app Rental, pas pour des ventes classiques : ne pas le généraliser.
- ✅ Les packagings sont propres à chaque produit et leurs codes-barres identifient un type, pas un exemplaire ; Odoo ne suit que la quantité totale, pas le nombre de packagings.

_Pistes à tester_
- Piste à tester : créer un produit de type service ou bien « Consigne palette » par type d'emballage, ajouté sur la commande avec la marchandise, puis rembourser par Credit Note au retour, en s'inspirant du flux de caution Rental.
- Piste à tester : suivre le solde de consignes par client via le rapport **Partner Ledger** en utilisant un compte comptable dédié aux consignes sur ces produits.
- Piste à tester : suivre les quantités d'emballages détenues par client via des Reverse Transfers sur un produit stockable « emballage ».

_Non couvert_
- Aucun passage ne décrit un flux natif de consigne d'emballages avec solde par client.
- Configuration comptable (compte de consigne, taxes) non couverte.
- Rapport dédié au solde de consignes par client non documenté.

_Sources :_ [1] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/owned_stock.html#enable-the-consignment-setting · [2] applications/inventory_and_mrp/inventory/product_management/configure/packaging.html · [3] applications/sales/sales/products_prices/returns.html#before-invoicing · [4] applications/sales/sales/products_prices/returns.html#after-invoicing · [5] applications/sales/rental/rental_orders/manage_deposits.html#app-integration-configuration · [6] applications/sales/rental/rental_orders/manage_deposits.html#refund-deposits-upon-return · [7] applications/inventory_and_mrp/inventory/product_management/configure.html#pallets-of-items-using-packaging · [8] applications/inventory_and_mrp/inventory/product_management/configure/package.html · [9] applications/inventory_and_mrp/inventory/product_management/configure/package.html#configuration · [11] applications/finance/accounting.html#accounts-receivable-and-payable

**Note A : ___**

### Réponse B

**Statut : À vérifier** · couverture partial

⚠️ La documentation fournie ne décrit pas de fonctionnalité native dédiée à la gestion complète des emballages consignés (palettes, fûts) vendus avec la marchandise et suivis en solde d'unités par client. Dans Odoo **Inventory**, le *packaging* désigne uniquement des contenants jetables et le système ne suit pas le nombre d'emballages ou de palettes en stock. Les passages documentent toutefois les retours physiques clients, le remboursement par avoir (**Credit Note**), le suivi du solde financier via le **Partner Ledger**, ainsi qu'un mécanisme de caution (**deposit**) propre à l'application **Rental**.

_Prérequis_
- ⚠️ L'application **Accounting** doit être installée pour émettre des avoirs (**Credit Notes**) lors du remboursement d'une consigne et pour consulter le rapport **Partner Ledger**.

_Étapes_
1. ✅ **Enregistrer le retour physique du client en stock** — Lorsqu'un client rapporte des biens gérés en stock, créez un retour à partir de la livraison d'origine afin de réintégrer les articles depuis l'emplacement *customer* vers votre stock (le retour est alors valorisé au coût unitaire de sortie d'origine).
2. ✅ **Initier un avoir (Credit Note) pour le remboursement** — Allez dans **Accounting ‣ Customers ‣ Invoices**, ouvrez la facture d'origine concernée et cliquez sur **Credit Note**. Il est également possible de créer un avoir de zéro en allant dans **Accounting ‣ Customers ‣ Credit Notes** puis en cliquant sur **New**.
3. ✅ **Ajuster les quantités remboursées et confirmer l'avoir** — Dans la fenêtre **Credit Note**, renseignez le champ **Reason** et mettez à jour si besoin les champs **Journal** et **Reversal date**. Cliquez sur **Reverse** pour ouvrir un brouillon d'avoir prérempli, modifiez les champs **Product** et **Quantity** pour refléter uniquement les consignes retournées (remboursement partiel), puis cliquez sur **Confirm**.
4. ⚠️ **Consulter le solde financier par client** — Pour visualiser la balance comptable des clients (incluant les factures et avoirs liés à leurs contacts), accédez au rapport **Partner Ledger** via **Accounting ‣ Reporting ‣ Partner Ledger**.

_Attention_
- ✅ Ne confondez pas les emballages consignés avec l'option **Consignment** (**Inventory ‣ Configuration ‣ Settings**, section **Traceability**), qui sert à réceptionner, stocker et vendre du stock appartenant à un tiers sans en être propriétaire.
- ✅ La fonctionnalité **Units of Measure & Packagings** (**Inventory app ‣ Configuration ‣ Settings**, section **Products**) est conçue pour des contenants jetables spécifiques à un produit : Odoo ne comptabilise que la quantité totale d'unités du produit et ne suit pas le nombre de palettes ou d'emballages en stock.
- ✅ La configuration d'un produit de caution dédié (**Product Type** sur **Service** et **Invoicing Policy** sur **Based on Delivered Quantity (Manual)**) et son processus de remboursement sont documentés uniquement dans le cadre de l'application **Rental** (**Rental ‣ Products ‣ Products** et **Rental app ‣ Orders ‣ Orders**).

_Pistes à tester_
- Piste à tester : Créer les palettes et fûts consignés comme des produits stockables à part entière (et non comme des *packagings*), les ajouter sur une ligne dédiée des commandes de vente pour les livrer et les facturer avec la marchandise, puis gérer leur restitution via un retour sur le bon de livraison suivi d'un avoir (**Credit Note**).
- Piste à tester : Transposer le fonctionnement des cautions de l'application **Rental** aux commandes de vente standard en créant un produit avec **Product Type** défini sur **Service** et **Invoicing Policy** sur **Based on Delivered Quantity (Manual)**, puis en réduisant la quantité livrée (**Delivered**) sur la commande client lors du retour pour générer un avoir.
- Piste à tester : Utiliser un compte comptable dédié sur le produit de consigne afin d'isoler le solde financier des consignes par client lors de la consultation des rapports comptables comme le **Partner Ledger**.

_Non couvert_
- Mécanisme natif permettant d'ajouter automatiquement les lignes d'emballages consignés (palettes, fûts) sur la commande client en fonction des quantités de marchandises vendues.
- Suivi natif du solde en quantité physique d'emballages consignés détenus par chaque client (le rapport **Partner Ledger** ne présentant qu'un solde comptable en valeur).

_Sources :_ [1] applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/owned_stock.html#enable-the-consignment-setting · [2] applications/inventory_and_mrp/inventory/product_management/configure/packaging.html · [3] applications/sales/rental/rental_orders/manage_deposits.html#configuration · [5] applications/finance/accounting.html#accounts-receivable-and-payable · [6] applications/sales/rental/rental_orders/manage_deposits.html#refund-deposits-upon-return · [7] applications/inventory_and_mrp/inventory/product_management/configure.html#pallets-of-items-using-packaging · [8] applications/inventory_and_mrp/inventory/product_management/configure/packaging.html#configuration · [9] applications/sales/rental/rental_orders/manage_deposits.html#app-integration-configuration · [10] applications/inventory_and_mrp/inventory/inventory_valuation/operations_valuation.html#customer-returns · [11] applications/finance/accounting/customer_invoices.html#partner-ledger · [12] applications/finance/accounting/customer_invoices/credit_notes.html#issue-a-customer-credit-note

**Note B : ___**

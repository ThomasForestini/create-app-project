# Grille de relecture — corrigé QCM (30 questions)

> Générée par `scripts/qcm-grille.py`. Validées : **30/30**.
> Pour chaque question : vérifier la réponse proposée (doc v20 ou runbot.odoo.com, admin/admin), corriger `bonnes_reponses` dans `corrige.json` si besoin, puis passer `valide` à `true`.

**À vérifier en priorité sur runbot ou à confiance moyenne/faible (8)** : Q01, Q06, Q11, Q18, Q21, Q22, Q24, Q26

## Q01 — Introduction (P002, p. 1)

**If you were in any list view, how would you display 1,000 records at once?**

- A. All records are always displayed.
- B. By clicking on the page indicator next to the view options ✅
- C. 80 records is the maximum number of results that can be displayed in list view.

- Proposé : **B** · méthode doc · confiance moyenne
- Source : https://www.odoo.com/documentation/20.0/applications/essentials/search.html
- Note : Cliquer sur l'indicateur de pagination d'une vue liste et saisir une plage allant jusqu'à 1 000. La documentation v20 citée ne décrit pas ce geste ; confirmation indirecte par le forum Odoo, sans essai runbot.
- Rémy (info) : B vert (sa réponse)
- [x] Validé par Thomas

## Q02 — Introduction (P003, p. 1)

**How do you access the technical menu?**

- A. Go to the Settings module and it automatically appears there.
- B. Load the technical module from the Apps module and it will be accessible.
- C. Activate developer mode and go to the Settings module. ✅

- Proposé : **C** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/general/developer_mode.html#developer-tools-and-technical-menu
- Note : « Database administrators can access the technical menu from the Settings app » une fois le mode développeur activé.
- Rémy (info) : C vert (sa réponse)
- [x] Validé par Thomas

## Q03 — Sales (P010, p. 3)

**A customer is linked to the pricelist 'Retailer.' If you create a quote for this customer, but change the pricelist to 'Consumer' before adding products to the quote, what price will be used for the new sale order lines?**

- A. A price from the 'Retailer' pricelist
- B. A price from the 'Consumer' pricelist ✅
- C. The system issue a warning, and request the correct pricelist be applied

- Proposé : **B** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/sales/sales/sales_quotations/margin.html#margin-calculation-with-a-pricelist
- Note : Les lignes ajoutées après la modification utilisent la liste de prix du devis, ici Consumer, et non la liste Retailer de la fiche client.
- Rémy (info) : B vert (sa réponse)
- [x] Validé par Thomas

## Q04 — Sales (P016, p. 4)

**During the sales process, when is the on-hand quantity of a product decreased in your inventory?**

- A. When the delivery order is validated ✅
- B. When the sales order is validated
- C. When the customer invoice is paid

- Proposé : **A** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/inventory_and_mrp/inventory/shipping_receiving/daily_operations/receipts_delivery_one_step.html#deliver-goods-directly-1-step
- Note : La quantité en stock diminue lors de la validation du bon de livraison. La confirmation de la commande crée la livraison et peut modifier le prévisionnel, sans réduire à elle seule le stock disponible.
- Rémy (info) : A vert (sa réponse)
- [x] Validé par Thomas

## Q05 — Survey (P017, p. 5)

**Can the survey participant be directed to a specific question based on their answer to a previous question?**

- A. Yes. It's called 'Parent Questions.' (Go to the Question > Settings tab > Determine Parent Question & Child Answer)
- B. Yes. It's called 'Conditional Display'. (Go to the Question > Options tab > Locate the 'Conditional Display' section > Choose a Triggering Answer) ✅
- C. Yes, but only in a "Live Session" survey when the "Allow Roaming" feature is enabled.

- Proposé : **B** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/marketing/surveys/questions.html#conditional-display-section
- Note : Options tab ‣ Conditional Display ‣ Triggering Answers.
- Rémy (info) : B vert (sa réponse)
- [x] Validé par Thomas

## Q06 — CRM (P025, p. 6)

**If the manager of the Pre-Sales team creates a new property field on an opportunity, who can see it?**

- A. Only members of the Pre-Sales team.
- B. Only managers of other sales teams.
- C. Anyone with access to that opportunity. ✅

- Proposé : **C** · méthode doc · confiance moyenne
- Source : https://www.odoo.com/documentation/20.0/applications/essentials/property_fields.html#properties-across-apps
- Note : La propriété est liée à l'équipe commerciale ; elle est visible sur les opportunités concernées pour toute personne ayant accès à ces opportunités, sans restriction aux seuls managers.
- Rémy (info) : C vert (sa réponse)
- [x] Validé par Thomas

## Q07 — AI (P031, p. 8)

**What does it mean when an AI Agent is not assigned any Topics?**

- A. The agent can provide information, but cannot make changes to the database or perform tasks. ✅
- B. The agent can only perform tasks based on the information provided in its Sources.
- C. Leaving the Topics field empty means the agent has access to all topics and tools in the database.

- Proposé : **A** · méthode doc · confiance haute · ⚠️ écart v19/v20
- Source : https://www.odoo.com/documentation/20.0/applications/productivity/ai/agents.html#skills
- Note : v20 : les « Topics » s'appellent « Skills ». Sans skill, l'agent ne fait que fournir de l'information.
- Rémy (info) : A vert (sa réponse)
- [x] Validé par Thomas

## Q08 — AI (P033, p. 8)

**You want to ask an AI Agent how many leads are currently assigned to a specific salesperson. Which Topic must be assigned to the agent for it to answer that question?**

- A. Information Reporting.
- B. Information Retrieval. ✅
- C. Lead Assessment.

- Proposé : **B** · méthode doc · confiance haute · ⚠️ écart v19/v20
- Source : https://www.odoo.com/documentation/20.0/applications/productivity/ai/agents.html#skills
- Note : Skill préconfiguré « Information retrieval » (Topic en v19).
- Rémy (info) : B vert (sa réponse)
- [x] Validé par Thomas

## Q09 — Marketing (P036, p. 9)

**Can you use the same mailing list contacts for BOTH email and SMS marketing campaigns?**

- A. No, mailing list contacts are specific to the delivery method, and are not interchangeable.
- B. No, since SMS mailing list contacts do not have an email field, and email marketing lists do not have a phone number field.
- C. Yes, since mailing list contacts contain both email addresses and phone numbers. ✅

- Proposé : **C** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/marketing/email_marketing/mailing_lists.html#create-mailing-lists
- Note : Une même liste a les boutons Send Mailing et Send SMS ; Mailing Contacts partagé entre Email et SMS Marketing.
- Rémy (info) : C vert (sa réponse)
- [x] Validé par Thomas

## Q10 — Website (P041, p. 10)

**How can you hide the header and/or footer on pages?**

- A. You can do this upon activating developer mode.
- B. You can do this in the website editor, in the Styles tab. ✅
- C. You can do this in the website editor, in the Blocks tab.

- Proposé : **B** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/websites/website/structure/header_footer.html#header-and-footer-design
- Note : Style tab : Header Position = Hidden ; footer : Page visibility.
- Rémy (info) : B bleu (réponse alternative), C orange (erreur probable)
- [x] Validé par Thomas

## Q11 — Ecommerce (P043, p. 11)

**How can you edit the way the variant selection will be displayed on a website product page?**

- A. By clicking the attribute and changing the Block display type in the Style tab in the website editor.
- B. By changing the attribute display type in the Style tab. ✅
- C. By activating developer mode and going to the Theme tab in the website editor.

- Proposé : **B** · méthode doc · confiance moyenne
- Source : https://www.odoo.com/documentation/20.0/applications/sales/sales/products_prices/products/variants.html#attributes
- Note : B est le meilleur choix parmi les trois : c'est le Display Type de l'attribut qui détermine la présentation des variantes. Réserve : la documentation v20 situe ce réglage sur la fiche de l'attribut (Ventes > Produits > Attributs), et non explicitement dans l'onglet Style de l'éditeur web. Le « Block display type » de A ne désigne pas ce réglage.
- Rémy (info) : A vert (sa réponse) · **≠ proposé**
- [x] Validé par Thomas

## Q12 — Knowledge (P046, p. 11)

**Which of the following commands are exclusive to Knowledge?**

- A. Index, Item Kanban/Cards/List/Calendar ✅
- B. Separator, Checklist, Quote, Media, Emoji
- C. Banner Info/Success/Warning/Danger

- Proposé : **A** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/productivity/knowledge.html#commands
- Note : Commandes exclusives Knowledge : Index, Item Kanban/Cards/List/Calendar, Clipboard, Foldable Section, Article.
- Rémy (info) : A vert (sa réponse)
- [x] Validé par Thomas

## Q13 — Knowledge (P048, p. 12)

**After pressing CTRL+K, which symbol allows you to search for hidden articles?**

- A. The question mark (?)
- B. The dollar sign ($) ✅
- C. The exclamation mark (!)

- Proposé : **B** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/productivity/knowledge.html#basic-management
- Note : CTRL/CMD + K puis « ? » pour les articles visibles, « $ » pour les articles masqués.
- Rémy (info) : A vert (sa réponse) · **≠ proposé**
- [x] Validé par Thomas

## Q14 — Project (P053, p. 13)

**When is a milestone displayed in green?**

- A. When the milestone's deadline is today
- B. When all its tasks have been marked as done or canceled ✅
- C. When the milestone is marked as reached

- Proposé : **B** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/services/project/project_management/project_dashboard.html#milestones
- Note : Vert = prêt à être marqué atteint (tâches liées done ou canceled).
- [x] Validé par Thomas

## Q15 — Project (P056, p. 13)

**When creating a task from a project's Kanban view, adding "#priority" to the title will:**

- A. Add a "priority" tag to the task ✅
- B. Set's the task's priority to high
- C. Add the text "#priority" to the task's title

- Proposé : **A** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/services/project/tasks/task_creation.html#task-configuration
- Note : « #tags » ajoute des étiquettes ; « ! » met la priorité haute.
- [x] Validé par Thomas

## Q16 — Timesheets (P059, p. 14)

**At which level do you define a billing time target?**

- A. At the company level
- B. At the employee level ✅
- C. At the project level

- Proposé : **B** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/services/timesheets/billing_rates.html#configuration
- Note : Billing Time Target sur la fiche employé, onglet Settings.
- [x] Validé par Thomas

## Q17 — Accounting (P067, p. 15)

**Which feature allows you to automatically change the income or expense account that a product should use based on the customer or vendor?**

- A. Fiscal Positions. ✅
- B. Fiscal Localizations.
- C. Account Groups.

- Proposé : **A** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/finance/accounting/taxes/fiscal_positions.html
- Note : Les positions fiscales adaptent taxes et comptes de revenus/charges.
- [x] Validé par Thomas

## Q18 — Accounting (P068, p. 16)

**What happens when you try to confirm a bill with an Accounting Date before the Lock Tax Return date?**

- A. Odoo will only allow users with Administrator access rights for the Accounting application to confirm the bill. All other users will receive a validation error explaining that the tax period is locked and the bill cannot be confirmed.
- B. Odoo will allow you to post the bill, but it will alert you that the tax period is locked and the bill should be reviewed.
- C. Odoo will automatically set the Accounting Date to today. ✅

- Proposé : **C** · méthode doc · confiance faible
- Source : https://www.odoo.com/documentation/20.0/applications/finance/accounting/reporting/tax_returns.html#tax-return-lock-date
- Note : C est le choix le plus proche car Odoo ajuste automatiquement la date comptable d'une facture placée dans une période verrouillée. Attention : « today » n'est pas une règle générale ; la date est reportée à une période ouverte (selon le verrou et le journal). La documentation fiscale v20 indique aussi le report des valeurs de taxe. A et B ne décrivent pas correctement ce mécanisme ; aucun choix n'est parfaitement exact.
- [x] Validé par Thomas

## Q19 — Spreadsheet (P077, p. 18)

**When you upload an Excel or CSV file and open it with Odoo Spreadsheet, what happens to the original file?**

- A. By default, it is deleted, but you can opt to preserve the file. ✅
- B. The original file is moved to an 'Uploaded Files' folder.
- C. By default, it is preserved in the same folder unless you check 'Send source file to trash'.

- Proposé : **A** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/productivity/spreadsheet/get_started.html#upload-files
- Note : Par défaut, le fichier source est supprimé ; décocher « Send source file to trash » pour le garder.
- [x] Validé par Thomas

## Q20 — Spreadsheet (P079, p. 18)

**In a spreadsheet containing dynamic Odoo data, how can you access an underlying database record, e.g., a specific sales order?**

- A. By right-clicking the cell and selecting 'See record'. ✅
- B. By selecting the cell, then clicking 'View' then 'Show' from the menu bar.
- C. By double clicking the cell.

- Proposé : **A** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/productivity/spreadsheet/insert.html#accessing-underlying-data
- Note : Clic droit ‣ See record.
- [x] Validé par Thomas

## Q21 — HR (P083, p. 19)

**Is it possible for employees to view the onboarding slides in the Referrals app after they've already seen them?**

- A. Yes, by going to 'Referrals' app > 'Configuration' > 'Onboarding' and click 'Restart Onboarding'.
- B. Yes, by setting the 'Onboarding' option to 'always show'.
- C. No, they can only be viewed once and cannot be shown again. ✅

- Proposé : **C** · méthode doc · confiance moyenne
- Source : https://www.odoo.com/documentation/20.0/applications/hr/referrals.html#onboarding
- Note : Après « Start Now », les diapositives d'accueil de Referrals ne sont plus montrées à l'employé. Le menu de configuration sert à modifier l'accueil, pas à le relancer pour lui.
- [x] Validé par Thomas

## Q22 — HR (P084, p. 19)

**How can a user with the required rights change an Employee's presence in the database from Present to Absent?**

- A. In the Attendances app dashboard, click on the employee
- B. In the Employees app dashboard, click Presence Icon > Absent ✅
- C. On the Employee record, click Actions > Presence Control > Set Absent

- Proposé : **B** · méthode doc · confiance moyenne
- Source : https://www.odoo.com/documentation/20.0/applications/hr/employees.html
- Note : Le contrôle manuel de présence passe par la carte employé en vue Kanban de l'application Employés et son icône de présence ; choisir Absent. Le cours officiel Odoo confirme l'usage de la vue Kanban pour ajuster la présence. La documentation v20 ne détaille pas ce clic exact ; runbot était inaccessible.
- [x] Validé par Thomas

## Q23 — POS (P085, p. 20)

**What are the preconfigured presets for a restaurant?**

- A. Delivery, Dine In, and Takeout. ✅
- B. Pickup, Eat In, and Online delivery.
- C. Food truck, Restaurant, and Uber.

- Proposé : **A** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/sales/point_of_sale/extra/presets.html
- Note : Les trois types de service proposés pour un restaurant sont Dine In, Takeout et Delivery.
- [x] Validé par Thomas

## Q24 — POS (P087, p. 20)

**If no payment method is selected, what is the default one in the register?**

- A. Cash. ✅
- B. Card.
- C. Customer account.

- Proposé : **A** · méthode doc · confiance moyenne
- Source : https://www.odoo.com/documentation/20.0/applications/sales/point_of_sale/payment_methods.html
- Note : Cash est sélectionné par défaut si un montant est saisi sans choisir de moyen de paiement. Cette règle est explicite dans la documentation officielle Odoo 18 ; la page v20 citée décrit les moyens de paiement mais ne répète pas cette phrase. Pas d'essai runbot possible.
- [x] Validé par Thomas

## Q25 — Purchase (P088, p. 20)

**Where do you define the vendor delivery lead time?**

- A. On the Product form, go to the Purchase tab
- B. Go to Purchase > Configuration > Vendor Pricelists
- C. Both options above are places to define vendor lead time ✅

- Proposé : **C** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/inventory_and_mrp/purchase/manage_deals/rfq.html#vendor-pricelist
- Note : Delivery Lead Time dans l'onglet Purchase du produit, ou Purchase ‣ Configuration ‣ Vendor Pricelists.
- [x] Validé par Thomas

## Q26 — Inventory (P100, p. 23)

**What happens when the on-hand quantity of a product is manually updated to increase by 10 units?**

- A. Nothing; on-hand quantity can only be updated by following the purchasing process
- B. The forecasted quantity increases by 10 units
- C. The on-hand quantity updates to 10, and an inventory adjustment is created to account for the difference ✅

- Proposé : **C** · méthode doc · confiance moyenne
- Source : https://www.odoo.com/documentation/20.0/applications/inventory_and_mrp/inventory/warehouses_storage/inventory_management/count_products.html#create-an-inventory-adjustment
- Note : La modification manuelle de la quantité disponible produit un ajustement d'inventaire. C est le meilleur choix ; « updates to 10 » est imprécis si la quantité initiale n'est pas zéro : l'augmentation est de 10 unités, pas nécessairement un total de 10.
- [x] Validé par Thomas

## Q27 — Inventory (P105, p. 24)

**On which document can an expiration date be set for newly received products?**

- A. Purchase order
- B. Receipt ✅
- C. Either the purchase order or receipt

- Proposé : **B** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/inventory_and_mrp/inventory/product_management/product_tracking/expiration_dates.html#set-expiration-dates-on-receipts-with-lots-serial-numbers
- Note : Saisie sur la réception (Detailed Operations, lot/série).
- [x] Validé par Thomas

## Q28 — MRP (P109, p. 25)

**Can you use a kit as a component in a bill of materials?**

- A. Yes ✅
- B. No
- C. Only when the 'BoM Kits' setting is enabled

- Proposé : **A** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/inventory_and_mrp/manufacturing/advanced_configuration/kit_shipping.html
- Note : Oui. Un kit peut organiser des composants dans une nomenclature plus complexe : sa nomenclature est imbriquée dans une autre nomenclature, sans réglage « BoM Kits » supplémentaire.
- Rémy (info) : A vert (sa réponse)
- [x] Validé par Thomas

## Q29 — MRP (P117, p. 27)

**What does it mean when a work center is operating at "reduced speed"?**

- A. The work center is operating more slowly than usual
- B. The work center does not have enough employees staffing
- C. The work center is processing a work order that has exceeded its expected duration ✅

- Proposé : **C** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/inventory_and_mrp/manufacturing/reporting/oee.html#reduced-speed
- Note : Mot pour mot dans la doc v20.
- Rémy (info) : C vert (sa réponse)
- [x] Validé par Thomas

## Q30 — STUDIO (P120, p. 27)

**What is the effect of editing the Footer content in the Report Editor?**

- A. The footer of all standard and custom reports is modified. ✅
- B. Only the footer of that specific report is modified.
- C. Only the footers of Internal reports are modified, not External reports.

- Proposé : **A** · méthode doc · confiance haute
- Source : https://www.odoo.com/documentation/20.0/applications/studio/pdf_reports.html#report-editor
- Note : « Editing the header and footer of a report impacts all standard and custom reports. »
- Rémy (info) : A bleu (réponse alternative)
- [x] Validé par Thomas

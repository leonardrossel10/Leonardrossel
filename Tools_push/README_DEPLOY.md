But: Déploiement simple

Pour déployer le site (normaliser le seed, régénérer les pages et pousser vers le remote) exécutez :

```bash
bash Tools_push/deploy.sh
```

Notes :
- Si votre dépôt utilise Git LFS, installez-le d'abord : `brew install git-lfs && git lfs install`.
- `Tools_push/push_photo.sh` utilisera `Tools_push/optimize_images.py` si présent, sinon l'optimisation est sautée.

Double-clic (macOS)

J'ai ajouté un helper `deploy.command` à la racine du projet. Pour pouvoir double-cliquer dessus depuis le Finder :

```bash
chmod +x deploy.command
```

Double-cliquez ensuite sur `deploy.command` — une fenêtre Terminal ouvrira et exécutera `Tools_push/deploy.sh`.

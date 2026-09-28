#!/bin/bash
echo "⬇️  Scarico da GitHub..."
git pull origin main --no-edit
echo "📦 Impacchetto le modifiche locali..."
git add .
git commit -m "sync: $(date '+%d/%m %H:%M')" || echo "→ nessuna modifica locale"
echo "⬆️  Carico su GitHub..."
git push origin main
echo "✅ Sync completata!"

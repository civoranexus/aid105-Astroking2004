#!/bin/bash
# Quick Render Deployment Checklist
# Run this to verify all files are in place

echo "🔍 Checking Render deployment files..."
echo ""

files_to_check=(
    "frontend/Dockerfile"
    "frontend/nginx.conf"
    "frontend/src/config.ts"
    "src/backend/Dockerfile"
    "src/backend/docker-entrypoint.sh"
    "render.yaml"
    "RENDER_DEPLOYMENT.md"
    "DEPLOYMENT_SUMMARY.md"
)

all_present=true

for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file - MISSING"
        all_present=false
    fi
done

echo ""
if [ "$all_present" = true ]; then
    echo "✅ All deployment files are in place!"
    echo ""
    echo "📋 Next steps:"
    echo "  1. git add ."
    echo "  2. git commit -m 'Add Render deployment configuration'"
    echo "  3. git push origin main"
    echo "  4. Go to https://render.com"
    echo "  5. Follow RENDER_DEPLOYMENT.md for step-by-step guide"
else
    echo "❌ Some files are missing. Please check the error messages above."
    exit 1
fi

const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const photosDir = path.join(__dirname, 'assets', 'photos');
const imagesDir = path.join(__dirname, 'assets', 'images');

// Responsive breakpoints (widths)
const BREAKPOINTS = [400, 800, 1200];

async function processImage(inputPath, outputDir, prefix) {
    const filename = path.basename(inputPath, path.extname(inputPath));
    const ext = path.extname(inputPath).toLowerCase();
    
    // Skip if not an image
    if (!['.jpg', '.jpeg', '.png', '.webp', '.gif'].includes(ext)) {
        console.log(`Skipping ${filename}${ext} (unsupported format)`);
        return [];
    }

    console.log(`Processing ${filename}${ext}...`);
    
    const generatedSizes = [];
    
    for (const width of BREAKPOINTS) {
        const outputPath = path.join(outputDir, `${prefix}${filename}-${width}w.webp`);
        
        try {
            await sharp(inputPath)
                .resize(width, null, { withoutEnlargement: true })
                .webp({ quality: 80 })
                .toFile(outputPath);
            
            const stats = fs.statSync(outputPath);
            const originalStats = fs.statSync(inputPath);
            const savings = ((1 - stats.size / originalStats.size) * 100).toFixed(1);
            
            generatedSizes.push({
                width,
                file: `${prefix}${filename}-${width}w.webp`,
                size: stats.size,
                savings
            });
            
            console.log(`  ✓ ${width}w: ${(stats.size / 1024).toFixed(1)}KB (${savings}% smaller)`);
        } catch (err) {
            console.error(`  ✗ Error processing ${width}w: ${err.message}`);
        }
    }
    
    // Also create a full-size WebP version
    const fullSizePath = path.join(outputDir, `${prefix}${filename}.webp`);
    try {
        await sharp(inputPath)
            .webp({ quality: 85 })
            .toFile(fullSizePath);
        
        const stats = fs.statSync(fullSizePath);
        const originalStats = fs.statSync(inputPath);
        const savings = ((1 - stats.size / originalStats.size) * 100).toFixed(1);
        
        generatedSizes.push({
            width: 'full',
            file: `${prefix}${filename}.webp`,
            size: stats.size,
            savings
        });
        
        console.log(`  ✓ full: ${(stats.size / 1024).toFixed(1)}KB (${savings}% smaller)`);
    } catch (err) {
        console.error(`  ✗ Error processing full: ${err.message}`);
    }
    
    return generatedSizes;
}

async function main() {
    console.log('🚀 Optimizing images for emirhnsenn.me\n');
    
    const allGenerated = [];
    
    // Process photos
    if (fs.existsSync(photosDir)) {
        const files = fs.readdirSync(photosDir);
        for (const file of files) {
            const filePath = path.join(photosDir, file);
            const stats = fs.statSync(filePath);
            if (stats.isFile()) {
                const sizes = await processImage(filePath, photosDir, '');
                allGenerated.push({ path: 'photos', file: path.basename(file, path.extname(file)), sizes });
            }
        }
    }
    
    // Process images
    if (fs.existsSync(imagesDir)) {
        const files = fs.readdirSync(imagesDir);
        for (const file of files) {
            const filePath = path.join(imagesDir, file);
            const stats = fs.statSync(filePath);
            if (stats.isFile()) {
                const sizes = await processImage(filePath, imagesDir, '');
                allGenerated.push({ path: 'images', file: path.basename(file, path.extname(file)), sizes });
            }
        }
    }
    
    // Generate srcset mapping JSON for HTML update
    const mappingPath = path.join(__dirname, 'srcset-mapping.json');
    fs.writeFileSync(mappingPath, JSON.stringify(allGenerated, null, 2));
    
    console.log(`\n✅ Optimization complete!`);
    console.log(`📄 Mapping saved to: srcset-mapping.json`);
    
    // Print summary
    let totalSavings = 0;
    let count = 0;
    allGenerated.forEach(img => {
        img.sizes.forEach(s => {
            if (s.savings !== 'NaN') {
                totalSavings += parseFloat(s.savings);
                count++;
            }
        });
    });
    
    if (count > 0) {
        console.log(`📊 Average file size reduction: ${(totalSavings / count).toFixed(1)}%`);
    }
}

main().catch(console.error);

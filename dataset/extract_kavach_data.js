const fs = require('fs');
const path = require('path');

const kavachDataDir = 'C:\\Users\\Acer\\.gemini\\antigravity\\brain\\c9f84614-e3ba-49f2-8cd6-a3aef123653d\\scratch\\kavach_repo\\src\\data';

// Helper to eval ES-module JS data files by stripping export statements
function loadModuleFile(filename) {
    const filePath = path.join(kavachDataDir, filename);
    let code = fs.readFileSync(filePath, 'utf8');
    // Replace export default and export const
    code = code.replace(/export\s+default\s+([a-zA-Z0-9_]+);/g, 'module.exports = $1;');
    code = code.replace(/export\s+const\s+/g, 'const ');
    
    // Create temporary file in current directory to require
    const tempPath = path.join(__dirname, `_temp_${filename}`);
    fs.writeFileSync(tempPath, code, 'utf8');
    try {
        const mod = require(tempPath);
        fs.unlinkSync(tempPath);
        return mod;
    } catch (e) {
        if (fs.existsSync(tempPath)) fs.unlinkSync(tempPath);
        throw e;
    }
}

try {
    const questions = loadModuleFile('questions.js');
    const translations = loadModuleFile('translations.js');
    const videos = loadModuleFile('videos.js');

    const output = {
        categories: questions,
        translations: translations,
        videos: videos
    };

    const outPath = path.join(__dirname, 'kavach_data.json');
    fs.writeFileSync(outPath, JSON.stringify(output, null, 2), 'utf8');
    console.log(`Successfully extracted Kavach data to ${outPath}`);
    console.log(`Categories count: ${questions.length}`);
    console.log(`Videos count: ${videos.length}`);
} catch (err) {
    console.error('Error extracting Kavach data:', err);
    process.exit(1);
}


// Builds pages.html from pages.src.html, inlining the Inter Tight 600 "Aero." logo.
const fs=require('fs'),path=require('path');
const b='/home/claude/research/brand/fullstop-intertight600/';
const cur=s=>s.trim().replace(/fill="#1D1D1F"/g,'fill="currentColor"');
const LOGO=cur(fs.readFileSync(b+'lockup.svg','utf8')).replace('<svg ','<svg class="logo" ');
const MARK=cur(fs.readFileSync(b+'mark.svg','utf8')).replace('<svg ','<svg class="mk-a" ');
let s=fs.readFileSync(path.join(__dirname,'pages.src.html'),'utf8');
s=s.split('{{LOGO}}').join(LOGO).split('{{MARK_JS}}').join(MARK).split('{{MARK}}').join(MARK);
fs.writeFileSync(path.join(__dirname,'pages.html'),s);console.log('pages.html',(s.length/1024).toFixed(0)+' KB');

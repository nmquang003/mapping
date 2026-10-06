import {mkdir,cp,rm} from 'node:fs/promises';
await rm('dist',{recursive:true,force:true});await mkdir('dist');
for(const file of ['index.html','style.css','game.js','rules.js','assets'])await cp(file,`dist/${file}`,{recursive:true});
console.log('Static game built in dist/');

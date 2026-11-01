const fs = require('node:fs/promises');
const path = require('node:path');
const {chromium} = require(process.env.PLAYWRIGHT_CORE_PATH || 'playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_EXECUTABLE_PATH?{executablePath:process.env.CHROME_EXECUTABLE_PATH}:{})});
 try{
  const page=await browser.newPage({viewport:{width:1200,height:680},deviceScaleFactor:1});
  const folder=path.join(__dirname,'_frames/07-coin-cycle');
  for(const file of (await fs.readdir(folder)).filter(f=>f.endsWith('.svg')).sort()){
   await page.setContent('<body style="margin:0">'+await fs.readFile(path.join(folder,file),'utf8')+'</body>');
   await page.screenshot({path:path.join(folder,file.replace('.svg','.png'))});
  }
  for(const file of ['04-state-scope.svg','05-checkpoints.svg','06-pickup-cycle.svg']){
   await page.setContent('<body style="margin:0">'+await fs.readFile(path.join(__dirname,file),'utf8')+'</body>');
   const overflow=await page.evaluate(()=>[...document.querySelectorAll('svg text')].filter(t=>{const r=t.getBBox();return r.x<0||r.x+r.width>1200||r.y+r.height>680}).map(t=>t.textContent));
   if(overflow.length)throw Error('Diagram overflow: '+overflow.join('; '));
   await page.screenshot({path:path.join(__dirname,'_frames',file.replace('.svg','.png'))});
  }
 }finally{await browser.close()}
 console.log('Rendered 36 animation frames and 3 diagrams.');
})().catch(e=>{console.error(e.message);process.exitCode=1});

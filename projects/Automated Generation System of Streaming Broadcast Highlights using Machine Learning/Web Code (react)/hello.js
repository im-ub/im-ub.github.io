
import { url } from 'inspector';
import connect from 'C:/Users/KYJ/Desktop/url/web/src/components/Form';

// const {InputUrl} = require('C:/Users/KYJ/Desktop/url/web/src/components/Form');
export const hello = () => {
  const data = useMemo(() => connect, []);

  // console.log('%s',curStr);
  // console.dir(curURL);
}


const { spawn } = require ('child_process');

// childPython = spawn ('python' , ['--version']);
const childPython = spawn('python',['codespace.py',url,'hxr989pss9azzdbzfrlwhwbcabjhp2']);
// obj = { Channel: 'Oyekool' }
// const childPython = spawn('python',['codespace.py' , JSON.stringify(obj)]);


childPython.stdout.on ('data', (data) => {
  console.log (`stdout: ${data}`);
});

childPython.stderr.on ('data', (data) => {
    console.log (`stderr: ${data}`);
  });
  
  childPython.on ('close', (code) => {
    console.log (`child process exited with code ${code}`);
  });

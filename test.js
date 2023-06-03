function findMode(arr) {
    if (arr.length === 0) {
      return false;
    }
    const frequencyCounter = {};
    for (let num of arr) {
      frequencyCounter[num] = (frequencyCounter[num] || 0) + 1;
    }
    let maxFrequency = 0;
    for (let key in frequencyCounter) {
      if (frequencyCounter[key] > maxFrequency) {
        maxFrequency = frequencyCounter[key];
      }
    }
    const modes = [];
    for (let key in frequencyCounter) {
      if (frequencyCounter[key] === maxFrequency) {
        modes.push(Number(key));
      }
    }
  
    if (modes.length === Object.keys(frequencyCounter).length) {
      return false;
    }
  
    return modes;
  }
const array = [1, 2, 3, 3, 4, 5, 5, 4, 3, 4, 2, 3,4 ,5 ,4, 3, 2, 3,4 ,2 ,3, 4];
const mode = findMode(array);
console.log(mode); // Output: [5]